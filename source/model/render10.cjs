const {chromium}=require('C:/Users/39015/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
(async()=>{const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const page=await browser.newPage({viewport:{width:1600,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8766/revision12/index.html');await page.waitForFunction(()=>window.modelReady,null,{timeout:60000});
const floors=[];for(const floor of ['1','2','3']){await page.evaluate(f=>window.setFloor(f),floor);await page.waitForTimeout(350);floors.push(await page.evaluate(()=>({planes:renderer.clippingPlanes.map(p=>({normal:p.normal.toArray(),constant:p.constant}))})));await page.screenshot({path:path.join(__dirname,'floor-'+floor+'.png')});}
await page.evaluate(()=>window.setView('passage'));await page.waitForTimeout(350);await page.screenshot({path:path.join(__dirname,'passage-open.png')});
await page.evaluate(()=>{window.setView('west');camera.position.set(-138,11,48);controls.target.set(-115,7,28);controls.update()});await page.waitForTimeout(350);await page.screenshot({path:path.join(__dirname,'west-stair.png')});
fs.writeFileSync(path.join(__dirname,'floor-ui-validation.json'),JSON.stringify({errors,floors},null,2));console.log({errors,floors: floors.length});await browser.close();})();
