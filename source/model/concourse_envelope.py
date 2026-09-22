"""Rebuild concourse weather envelope and map-anchored bridge joints at final heights.
Loaded after the legacy level transform. Satellite-derived west footprint; heights estimated.
"""
def repair_concourse(ns):
    import json
    import math
    import numpy as np
    groups, mapping = ns['groups'], ns['mapping']
    box, mesh, beam, wallhole = [ns[k] for k in ('box','mesh','beam','wallhole')]
    metal, frame, glass, floor, white = [ns[k] for k in ('METAL','FRAME','GLASS','FLOOR','WHITE')]
    level = ns['FG']
    obsolete = {'Facade_ConcourseEnds','Facade_GateDoorHeaders','Facade_GateDoorPanels',
                'Facade_GateDoorFrames','Facade_ConcoursePortholes','Facade_CladdingSeams',
                'Roof_ConcourseCurves','Facade_ConcourseCurves','Exterior_ConcourseHorizontalSeams',
                'Facade_Gate17Annex','Roof_Gate17Annex','Structure_Gate17Annex'}
    for key in list(groups):
        if key[0] in obsolete or key[0].startswith('Exterior_JetBridge_'):
            del groups[key]
    ways = [w for w in mapping['ways'] if w['tags'].get('aeroway') == 'jet_bridge']
    roots = sorted((float(p[0]), str(w['tags']['ref'])) for w in ways for p in w['points']
                   if -15 < p[1] < -10 and p[0] < 383)
    door_half = 1.65
    portal_top = level + 3.3
    def subtract_intervals(a,b,holes):
        spans=[(a,b)]
        for left,right in holes:
            spans=[s for c,d in spans for s in ((c,min(d,left)),(max(c,right),d)) if s[1]-s[0]>1e-5]
        return spans
    def prism(name, mat, polygon, bottom, top):
        # Convex polygons or individual triangles only.
        n=len(polygon)
        vv=[(x,y,z) for y in (bottom,top) for x,z in polygon]
        ff=[(0,i+1,i) for i in range(1,n-1)]+[(n,n+i,n+i+1) for i in range(1,n-1)]
        ff += [f for i in range(n) for f in ((i,(i+1)%n,(i+1)%n+n),(i,(i+1)%n+n,i+n))]
        mesh(name,mat,vv,ff)
    # The user requests an exterior-only west volume, with no passenger connection.
    west_open=(-384.,-341.)
    holes=[(x-door_half,x+door_half) for x,_ in roots]
    for side in (-1,1):
        z=side*12.5
        spans=[(-384.,383.)] if side<0 else [(-384.,ns['X0']),(ns['X1'],383.)]
        cuts=holes if side<0 else []
        for left,right in spans:
            # Fill each module exactly to the shared boundary: no pitch overhang at ends.
            edges=list(np.arange(left,right,4.5))+[right]
            for a,b in zip(edges,edges[1:]):
                overlap=any(a<d and b>c for c,d in cuts)
                if not overlap:
                    wallhole('Facade_ConcoursePortholes',metal,(a+b)/2,level+2.7,z,b-a,4.2,min(3.4,b-a-.24),3.4,False)
                else:
                    for c,d in subtract_intervals(a,b,cuts):
                        box('Facade_GatePortalWall',metal,((c+d)/2,level+2.7,z),(d-c,4.2,.25))
                    box('Facade_GatePortalHeader',metal,((a+b)/2,(portal_top+level+4.8)/2,z),(b-a,level+4.8-portal_top,.25))
            for top in (False,True):
                for t0,t1 in zip(np.linspace(0,math.pi/2,17),np.linspace(0,math.pi/2,17)[1:]):
                    def yz(t):
                        return (level+4.8+1.05*math.sin(t) if top else level+.6-1.05*math.sin(t),side*(11.45+1.05*math.cos(t)))
                    y0,z0=yz(t0);y1,z1=yz(t1)
                    for a,b in ([(left,right)] if top else subtract_intervals(left,right,cuts)):
                        mesh('Roof_ConcourseCurves' if top else 'Facade_ConcourseCurves',metal,[(a,y0,z0),(b,y0,z0),(b,y1,z1),(a,y1,z1)],[(0,1,2),(0,2,3)])
    # End caps meet floor and roof. East passage leads into the enclosed gate-17 annex.
    box('Facade_ConcourseWestEnd',metal,(-384,level+2.91,0),(.24,5.82,25))
    for a,b in [(-12.5,-5.5),(7.5,12.5)]:
        box('Facade_ConcourseEastReturn',metal,(383,level+2.91,(a+b)/2),(.24,5.82,b-a))
    box('Facade_ConcourseEastLintel',metal,(383,level+4.8,1),(.24,2.04,13))
    box('Structure_Gate17Annex',floor,(402,level-.2,1),(39,.4,30))
    box('Roof_Gate17Annex',metal,(402,level+4.7,1),(39,.25,30))
    box('Facade_Gate17EastWall',glass,(421.5,level+2.3,1),(.2,4.6,30))
    box('Facade_Gate17RearWall',glass,(402,level+2.3,16),(39,4.6,.2))
    for a,b in [(382.5,415.93),(419.23,421.5)]:
        box('Facade_Gate17ApronWall',glass,((a+b)/2,level+2.3,-14),(b-a,4.6,.2))
    box('Facade_Gate17PortalHeader',metal,(417.58,level+3.95,-14),(3.3,1.3,.2))
    for a,b in [(-14,-12.5),(12.5,16)]:
        box('Facade_Gate17RearReturn',metal,(382.5,level+2.3,(a+b)/2),(.2,4.6,b-a))
    for z in np.arange(-14,16.01,3):
        box('Facade_Gate17Mullions',white,(421.5,level+2.3,z),(.25,4.6,.09))
    # Bridge walls, floor and roof share mitered section vertices at bends.
    report=[]
    for index,way in enumerate(ways):
        pts=np.array(way['points'],float)
        root_index=next((i for i,p in enumerate(pts) if -15<p[1]<-10),None)
        if root_index==len(pts)-1:pts=pts[::-1].copy();root_index=0
        if root_index is not None:
            assert root_index==0
            pts[0,1]=-14 if pts[0,0]>383 else -12.5
            # Survey noise at the short wall connection must not skew the frame.
            pts[1,0]=pts[0,0]
        directions=np.diff(pts,axis=0);directions/=np.linalg.norm(directions,axis=1)[:,None]
        normals=np.stack([-directions[:,1],directions[:,0]],axis=1)
        offsets=[]
        for i in range(len(pts)):
            if i==0:offsets.append(normals[0])
            elif i==len(pts)-1:offsets.append(normals[-1])
            else:
                m=normals[i-1]+normals[i];m/=np.linalg.norm(m)
                offsets.append(m/max(.2,float(m@normals[i])))
        offsets=np.array(offsets)
        for i,(a,b) in enumerate(zip(pts,pts[1:])):
            name='Exterior_JetBridge_'+str(way['tags']['ref'])+'_'+str(index)
            def strip(half):return [a-offsets[i]*half,b-offsets[i+1]*half,b+offsets[i+1]*half,a+offsets[i]*half]
            prism(name+'_Floor',floor,strip(1.65),level-.25,level)
            prism('Roof_JetBridge_'+str(index),metal,strip(1.77),portal_top,portal_top+.18)
            for side in (-1,1):
                q=[a+offsets[i]*(side*1.65-.045),b+offsets[i+1]*(side*1.65-.045),b+offsets[i+1]*(side*1.65+.045),a+offsets[i]*(side*1.65+.045)]
                prism(name+'_Wall',glass,q,level,portal_top)
                for t in np.linspace(0,1,max(2,int(np.linalg.norm(b-a)/1.8)+1)):
                    p=(a+side*offsets[i]*1.65)*(1-t)+(b+side*offsets[i+1]*1.65)*t
                    box(name+'_Mullion',white,(p[0],(level+portal_top)/2,p[1]),(.09,portal_top-level,.09))
            for p in (a,b):ns['rod'](name+'_Support',frame,(p[0],.3,p[1]),(p[0],level-.25,p[1]),.20,10)
        if root_index is not None:
            x,z=pts[0]
            for side in (-1,1):box('Facade_GateInterfaceJamb',frame,(x+side*1.7,(level+portal_top)/2,z),(.10,portal_top-level,.38))
            box('Facade_GateInterfaceFlashing',metal,(x,portal_top+.1,z),(3.65,.2,.45))
            box('Structure_GateInterfaceThreshold',floor,(x,level-.10,z),(3.3,.2,.6))
            report.append({'gate':str(way['tags']['ref']),'root':[float(x),level,float(z)],'clear_width':3.2,'clear_height':3.3})
    # Roof footprint traced on the georeferenced west satellite image. No invented windows.
    poly=[(-384,-12.5),(-424.86,-93.27),(-424.64,-120.05),(-414.04,-120.90),(-380.61,-52.31),(-371.37,-41.11),(-360.28,-32.71),(-347.42,-27.88),(-341,-12.5)]
    # Ear clipping handles the concave bend without a triangle fan crossing outside.
    def triangulate(poly):
        p=np.array(poly);indices=list(range(len(p)));out=[]
        cross=lambda a,b:float(a[0]*b[1]-a[1]*b[0])
        if sum(cross(a,b) for a,b in zip(p,np.roll(p,-1,axis=0)))<0:indices.reverse()
        while len(indices)>3:
            for j in range(len(indices)):
                a,b,c=[indices[k%len(indices)] for k in (j-1,j,j+1)]
                if cross(p[b]-p[a],p[c]-p[b])<=1e-8:continue
                if any(all(cross(p[v]-p[u],p[k]-p[u])>=-1e-8 for u,v in [(a,b),(b,c),(c,a)]) for k in indices if k not in (a,b,c)):continue
                out.append((a,b,c));indices.pop(j);break
            else:raise ValueError('West footprint is not simple')
        return out+[tuple(indices)]
    for tri in triangulate(poly):
        prism('Structure_WestReturnFloor',floor,[poly[i] for i in tri],level-.3,level)
        prism('Roof_WestReturn',metal,[poly[i] for i in tri],level+3.3,level+3.5)
    for a,b in zip(poly[:-1],poly[1:]):
        beam('Facade_WestReturnWall',metal,(a[0],level+1.65,a[1]),(b[0],level+1.65,b[1]),.2,3.3)
    # Close the boundary with the concourse; exterior-only volume is not navigable.
    beam('Facade_WestReturnClosure',metal,(-384,level+1.65,-12.62),(-341,level+1.65,-12.62),.2,3.3)
    for p in poly[::2]:box('Structure_WestReturnSupport',white,(p[0],(level-.3)/2,p[1]),(.55,level-.3,.55))
    (ns['ROOT']/'concourse-repair.json').write_text(json.dumps({'portals':report,'west_footprint':poly,'evidence':['references/t3-west-satellite.jpg','references/t3-west-satellite.json','references/exterior-airside.jpg','references/official-departure-map.jpg'],'limitations':'Satellite roof trace is approximate; west return heights and opaque facade treatment are estimates, not surveyed details.'},indent=2),encoding='utf-8')

repair_concourse(globals())
