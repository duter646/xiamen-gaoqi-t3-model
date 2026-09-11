"""Verify evidence freshness, not architectural correctness. Python stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def validate(manifest_path):
    root = manifest_path.resolve().parent
    data = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    errors = []

    def file_hash(record, label):
        relative = record.get('path', '')
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
            errors.append(f'{label}: expected a relative file path')
            return None
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append(f'{label}: file missing or outside manifest directory')
            return None
        actual = sha256(path)
        if actual != record.get('sha256'):
            errors.append(f'{label}: missing or stale SHA-256')
        return actual

    artifacts = data.get('artifacts', {})
    if not isinstance(artifacts, dict) or not artifacts:
        raise ValueError('artifacts must be a nonempty object')
    current = {name: file_hash(record, f'artifact {name}') for name, record in artifacts.items()}
    required = data.get('required_checks', [])
    if not isinstance(required, list) or not required or any(not isinstance(x, str) or not x for x in required):
        raise ValueError('required_checks must be a nonempty list of IDs')
    if len(set(required)) != len(required):
        errors.append('duplicate required check IDs')
    checks = data.get('checks', [])
    if not isinstance(checks, list):
        raise ValueError('checks must be a list')
    seen = set()
    covered = set()
    for check in checks:
        identifier = check.get('id', '')
        if not isinstance(identifier, str) or not identifier or identifier in seen:
            errors.append('missing or duplicate check ID')
            continue
        seen.add(identifier)
        if check.get('status') != 'pass':
            errors.append(f'{identifier}: check has not passed')
        if not isinstance(check.get('scope'), str) or not check['scope'].strip():
            errors.append(f'{identifier}: missing inspection scope')
        snapshots = check.get('artifacts', {})
        if not isinstance(snapshots, dict) or not snapshots:
            errors.append(f'{identifier}: no inspected artifact hashes')
            snapshots = {}
        for name, snapshot in snapshots.items():
            if name not in current or current[name] is None or snapshot != current[name]:
                errors.append(f'{identifier}: stale or unknown inspected artifact {name}')
            else:
                covered.add(name)
        evidence = check.get('evidence', [])
        if not isinstance(evidence, list) or not evidence:
            errors.append(f'{identifier}: no evidence files')
            continue
        for index, record in enumerate(evidence):
            file_hash(record, f'{identifier} evidence {index}')
    for missing in set(required) - seen:
        errors.append(f'missing required check: {missing}')
    for name in set(artifacts) - covered:
        errors.append(f'artifact not covered by a current check: {name}')
    return {'passed': not errors, 'scope': 'file hashes and evidence associations only', 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.manifest)
    except (OSError, ValueError, TypeError, AttributeError) as error:
        result = {'passed': False, 'errors': [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
