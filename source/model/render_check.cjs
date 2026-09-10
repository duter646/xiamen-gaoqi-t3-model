const {chromium}=require('C:/Users/39015/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path'),fs=require('fs');
(async()=>{
const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true,args:['--disable-gpu-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const page=await browser.newPage({viewport:{width:1600,height:1000},deviceScaleFactor:1});let errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8766/revision10/index.html');await page.waitForFunction(()=>window.modelReady||window.modelError,null,{timeout:60000});
if(await page.evaluate(()=>window.modelError))throw Error(await page.evaluate(()=>window.modelError));
for(const view of ['passage','international','directarrival','footprints']){await page.evaluate(v=>window.setView(v),view);await page.waitForTimeout(700);await page.screenshot({path:path.join(__dirname,`preview-${view}.png`)});}
const result=await page.evaluate(()=>{let meshes=0,invalid=0;model.traverse(o=>{if(!o.isMesh)return;meshes++;for(let x of o.geometry.attributes.position.array)if(!Number.isFinite(x))invalid++;});return {meshes,invalid,webgl:renderer.getContext().getError()};});
fs.writeFileSync(path.join(__dirname,'browser-validation.json'),JSON.stringify({errors,...result},null,2));console.log({errors,...result});await browser.close();})();
