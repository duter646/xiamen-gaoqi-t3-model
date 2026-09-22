const {chromium}=require('C:/Users/39015/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const page=await browser.newPage({viewport:{width:1500,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const assert=(v,m)=>{if(!v)throw Error(m)};
 await page.goto('http://127.0.0.1:8766/tests/map-sections.html');
 for(const level of ['arrival','checkin','departure']){
  await page.selectOption('#floor',level);
  assert(await page.locator('.view.active').getAttribute('id')===level,'selected section');
  assert(await page.locator(`#${level} .low path`).count()>10,'actual low mesh slices');
  await page.locator('#walls').uncheck();assert(await page.locator(`#${level} .walls`).evaluate(g=>getComputedStyle(g).display)==='none','toggle');
  await page.locator('#reset').click();
 }
 await page.selectOption('#floor','checkin');await page.screenshot({path:path.join(__dirname,'map-sections-browser.png')});
 await page.goto('http://127.0.0.1:8766/');await page.waitForFunction(()=>window.modelReady&&window.routesReady,null,{timeout:120000});
 await page.locator('#panel-toggle').click();
 for(const level of ['1','2']){
  await page.locator('#panel-toggle').click();await page.locator(`[data-floor="${level}"]`).click();await page.locator('#panel-toggle').click();
  await page.waitForTimeout(700);await page.screenshot({path:path.join(__dirname,`model-floor-${level}.png`)});
 }
 assert(errors.length===0,errors.join('\n'));await browser.close();console.log({errors,sections:3,modelFloors:2});
})().catch(e=>{console.error(e);process.exit(1)});
