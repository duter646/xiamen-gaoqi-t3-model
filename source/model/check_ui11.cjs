const {chromium}=require('C:/Users/39015/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
(async()=>{const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});const page=await browser.newPage({viewport:{width:1600,height:1000}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8766/revision14/index.html');await page.waitForFunction(()=>window.modelReady,null,{timeout:90000});await page.evaluate(()=>window.showInternationalRoute());await page.waitForTimeout(400);await page.screenshot({path:path.join(__dirname,'international-route.png')});
const route=await page.evaluate(()=>({visible:window.internationalOverlay.visible,objects:window.internationalOverlay.children.length}));const floors=[];
for(const floor of ['1','2','3']){await page.click(`[data-floor="${floor}"]`);floors.push(await page.evaluate(()=>renderer.clippingPlanes.length));}
fs.writeFileSync(path.join(__dirname,'final-ui-validation.json'),JSON.stringify({errors,route,floors},null,2));console.log({errors,route,floors});await browser.close();})();
