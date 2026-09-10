const {chromium}=require('C:/Users/39015/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');const fs=require('fs'),path=require('path');
(async()=>{const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});const page=await browser.newPage({viewport:{width:1500,height:980}});const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(process.env.VIEWER_URL||'http://127.0.0.1:8766/index.html');await page.waitForFunction(()=>window.modelReady&&window.routesReady,null,{timeout:120000});
const assert=(v,m)=>{if(!v)throw Error(m)};
assert(await page.locator('[data-route]').count()===4,'four route controls');assert(await page.locator('#view option').count()===10,'ten views');
await page.screenshot({path:path.join(__dirname,'viewer-overall.png')});
for(const id of ['domestic-departure','international-departure','domestic-arrival','international-arrival']){await page.locator(`[data-route="${id}"]`).check();assert(await page.evaluate(id=>viewer.routeGroups.get(id).visible,id),'route visible '+id)}
await page.locator('#route-focus').click();await page.waitForTimeout(500);await page.screenshot({path:path.join(__dirname,'viewer-routes.png')});
await page.locator('[data-floor="2"]').click();assert(await page.evaluate(()=>viewer.routeGroups.get('domestic-departure').visible),'floor switch keeps route');
await page.selectOption('#view','hall');assert(await page.evaluate(()=>viewer.routeGroups.get('domestic-departure').visible),'view switch keeps route');
await page.locator('#route-clear').click();assert(await page.evaluate(()=>[...viewer.routeGroups.values()].every(g=>!g.visible)),'clear routes');assert(await page.locator('#route-focus').isDisabled(),'focus disabled after clear');
await page.selectOption('#view','front');await page.locator('canvas').click({position:{x:500,y:500}});
async function travel(shift){const start=await page.evaluate(()=>viewer.camera.position.toArray());if(shift)await page.keyboard.down('Shift');await page.keyboard.down('w');await page.waitForTimeout(1000);await page.keyboard.up('w');if(shift)await page.keyboard.up('Shift');const end=await page.evaluate(()=>viewer.camera.position.toArray());return Math.hypot(...end.map((v,i)=>v-start[i]));}
const normal=await travel(false),fast=await travel(true);console.log({normal,fast,errors,focus:await page.evaluate(()=>document.activeElement.tagName)});assert(normal>10,'normal movement increased');assert(fast>normal*1.8,'shift boost');
await page.locator('#panel-toggle').click();assert(await page.locator('#panel').isHidden(),'panel collapses');await page.locator('#panel-toggle').click();
await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(__dirname,'viewer-mobile.png')});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no mobile overflow');
assert(errors.length===0,errors.join('\n'));fs.writeFileSync(path.join(__dirname,'viewer-validation.json'),JSON.stringify({errors,routeControls:4,views:10,movementMetres:{normal,shift:fast},floorAndViewPreserveRoutes:true,mobileNoOverflow:true},null,2));await browser.close();console.log({errors,normal,fast});})().catch(e=>{console.error(e);process.exit(1)});

