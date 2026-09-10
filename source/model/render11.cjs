const {chromium}=require('C:/Users/39015/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
(async()=>{const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const page=await browser.newPage({viewport:{width:1600,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8766/revision14/index.html');await page.waitForFunction(()=>window.modelReady,null,{timeout:90000});
for(const view of ['international','end','hall','west','passage']){await page.evaluate(v=>window.setView(v),view);await page.waitForTimeout(500);await page.screenshot({path:path.join(__dirname,'review-'+view+'.png')});}
fs.writeFileSync(path.join(__dirname,'browser-validation.json'),JSON.stringify({errors},null,2));console.log({errors});await browser.close();})();
