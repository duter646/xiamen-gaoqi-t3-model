const {chromium}=require('C:/Users/39015/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try {
  const page=await browser.newPage({viewport:{width:1500,height:950}});
  await page.goto('http://127.0.0.1:8766/?view=security');
  await page.waitForFunction(()=>window.modelReady&&window.routesReady,null,{timeout:120000});
  await page.evaluate(()=>{const el=document.querySelector('#roof');el.checked=true;el.dispatchEvent(new Event('change'));});
  for(const [name,position,target] of [['shop',[-62,25,51],[-48,13,34]],['straight-guard',[109,34,51],[80,12,26]]]){
   await page.evaluate(({position,target})=>{viewer.controls.enableDamping=false;viewer.camera.position.set(...position);viewer.controls.target.set(...target);viewer.controls.update();},{position,target});
   await page.waitForTimeout(500);
   await page.screenshot({path:path.join(__dirname,name+'.png')});
  }
 } finally {await browser.close()}
})();



