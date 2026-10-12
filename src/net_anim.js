(function(){
var NS='http://www.w3.org/2000/svg',T=13,UID=0;
var CITY={zh:['香港','台北','曼谷','東京','倫敦','新加坡','吉隆坡','馬尼拉'],en:['Hong Kong','Taipei','Bangkok','Tokyo','London','Singapore','Kuala Lumpur','Manila']};
var FEAT=[2,3,4,1,5,6,7,0],MS=[.3,.54,.78,1];
var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function el(n,a,p){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
function cl(x){return x<0?0:x>1?1:x}
function ease(x){x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}
function sm(a,b,t){return ease((t-a)/(b-a))}
function pop(x){x=cl(x);var c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}
function Net(stage){
 var lang=stage.getAttribute('data-lang')==='en'?'en':'zh',sec=stage.closest('.net');
 var pills=sec.querySelectorAll('.net-pill'),steps=sec.querySelectorAll('.net-steps li, .net-flow .fl');
 var chips=[];
 var acc=0,run=false,last=0,raf=0,narrow=null,S,id='zn'+(UID++);
 function build(){
  narrow=stage.clientWidth<560;
  var W=narrow?360:760,H=narrow?330:320,cx=W/2,cy=H/2,rx=narrow?100:300,ry=narrow?112:114;
  stage.innerHTML='';S={arcs:[],checks:[],mer:[],dots:[],cx:cx,cy:cy};
  var svg=el('svg',{viewBox:'0 0 '+W+' '+H,role:'img','aria-label':stage.getAttribute('data-label')||'',focusable:'false'},stage);
  var d=el('defs',{},svg),pt=el('pattern',{id:id+'p',width:13,height:13,patternUnits:'userSpaceOnUse'},d);
  el('circle',{cx:6.5,cy:6.5,r:1.05,fill:'#fff'},pt);
  var rg=el('radialGradient',{id:id+'g'},d);el('stop',{offset:'0','stop-color':'#EEBF01','stop-opacity':'.38'},rg);el('stop',{offset:'1','stop-color':'#EEBF01','stop-opacity':'0'},rg);
  var fg=el('radialGradient',{id:id+'f'},d);el('stop',{offset:'.55','stop-color':'#fff','stop-opacity':'1'},fg);el('stop',{offset:'1','stop-color':'#fff','stop-opacity':'0'},fg);
  var mk=el('mask',{id:id+'m'},d);el('ellipse',{cx:cx,cy:cy,rx:rx+30,ry:ry+24,fill:'url(#'+id+'f)'},mk);
  el('rect',{x:0,y:0,width:W,height:H,fill:'url(#'+id+'p)',opacity:'.13',mask:'url(#'+id+'m)'},svg);
  var gl=el('g',{fill:'none',stroke:'#fff','stroke-opacity':'.09','stroke-width':'1'},svg);
  el('ellipse',{cx:cx,cy:cy,rx:rx,ry:ry},gl);el('ellipse',{cx:cx,cy:cy,rx:rx*.92,ry:ry*.5},gl);el('line',{x1:cx-rx,y1:cy,x2:cx+rx,y2:cy},gl);
  for(var k=0;k<3;k++)S.mer.push(el('ellipse',{cx:cx,cy:cy,rx:rx,ry:ry},gl));
  S.ring=el('circle',{cx:cx,cy:cy,r:30,fill:'none',stroke:'#EEBF01','stroke-width':'1.5'},svg);
  el('circle',{cx:cx,cy:cy,r:narrow?58:70,fill:'url(#'+id+'g)'},svg);
  var ga=el('g',{},svg),gt=el('g',{},svg),gp=el('g',{},svg),gc=el('g',{},svg);
  S.ga=ga;S.gt=gt;S.gp=gp;
  var names=CITY[lang],fs=narrow?(lang==='en'?11:12.5):13;
  for(var i=0;i<8;i++){
   var an=(-112.5+45*i)*Math.PI/180,c=Math.cos(an),s=Math.sin(an),px=cx+rx*c,py=cy+ry*s;
   var dx=px-cx,dy=py-cy,L=Math.sqrt(dx*dx+dy*dy),qx=(cx+px)/2-dy/L*L*.2,qy=(cy+py)/2+dx/L*L*.2;
   var dd='M'+cx+' '+cy+'Q'+qx.toFixed(1)+' '+qy.toFixed(1)+' '+px.toFixed(1)+' '+py.toFixed(1);
   var p=el('path',{d:dd,fill:'none',stroke:'#58C2C4','stroke-width':'1.4','stroke-linecap':'round',pathLength:'1','stroke-dasharray':'1','stroke-dashoffset':'1'},ga);
   var tr=el('path',{d:dd,fill:'none',stroke:'#EEBF01','stroke-width':'2.4','stroke-linecap':'round',pathLength:'1','stroke-dasharray':'1','stroke-dashoffset':'1',opacity:'0'},gt);
   var halo=el('circle',{cx:px,cy:py,r:5,fill:'none',stroke:'#EEBF01','stroke-width':'1.4',opacity:'0'},gc);
   var dot=el('circle',{cx:px,cy:py,r:4,fill:'#fff'},gc);
   var anc=c>.35?'start':c<-.35?'end':'middle',lx=px+c*13,ly=py+s*13+fs*.36;
   if(anc==='middle')ly+=s<0?-4:6;
   var lb=el('text',{x:lx.toFixed(1),y:ly.toFixed(1),'text-anchor':anc,'font-size':fs},gc);lb.textContent=names[i];
   var pu=el('circle',{r:3,fill:'#EEBF01',opacity:'0'},gp);
   S.arcs.push({p:p,tr:tr,len:p.getTotalLength(),dot:dot,halo:halo,lb:lb,pu:pu,x:px,y:py});
  }
  for(var m=0;m<4;m++){var g=el('g',{opacity:'0'},gp);el('circle',{r:7,fill:'#EEBF01'},g);el('path',{d:'M-3.2 0.2L-1 2.4L3.3-2.3',fill:'none',stroke:'#10374E','stroke-width':'1.9','stroke-linecap':'round','stroke-linejoin':'round'},g);S.checks.push(g)}
  S.comp=el('circle',{r:3.6,fill:'#EEBF01',opacity:'0'},gp);
  S.trav=el('circle',{r:5,fill:'#fff',stroke:'#0B2334','stroke-width':'1.5',opacity:'0'},gp);
  var w=narrow?48:62,h=narrow?36:46,bx=cx-w/2,by=cy-h/2-4,b=el('g',{},svg);
  el('path',{d:'M'+(bx+10)+' '+by+'h'+(w-20)+'a10 10 0 0 1 10 10v'+(h-20)+'a10 10 0 0 1-10 10h-'+(w/2-16)+'l-8 8l-2-8h-'+(w/2-14)+'a10 10 0 0 1-10-10v-'+(h-20)+'a10 10 0 0 1 10-10z',fill:'#10374E',stroke:'#EEBF01','stroke-width':'2'},b);
  for(k=0;k<3;k++)S.dots.push(el('circle',{cx:cx-(narrow?9:11)+(narrow?9:11)*k,cy:cy-4,r:narrow?2.6:3,fill:'#fff'},b));
  var zt=el('text',{x:cx,y:by+h+(narrow?22:24),'text-anchor':'middle','font-size':narrow?11:12,'class':'zn-brand'},svg);zt.textContent='ZDelp';
  S.rx=rx;S.ry=ry;
 }
 function render(t,still){
  var tl=t%T,f=FEAT[Math.floor(t/T)%8],fade=still?1:1-sm(12.3,12.9,tl),dimB=still?.55:sm(6.2,6.8,tl),A=S.arcs;
  for(var k=0;k<3;k++)S.mer[k].setAttribute('rx',(S.rx*Math.abs(Math.cos(t*.22+k*Math.PI/3))).toFixed(1));
  var rp=(t%2.4)/2.4;S.ring.setAttribute('r',(30+rp*(narrow?40:52)).toFixed(1));S.ring.setAttribute('opacity',(.55*(1-rp)).toFixed(2));
  for(k=0;k<3;k++)S.dots[k].setAttribute('opacity',(.45+.55*Math.max(0,Math.sin(t*5-k*.9))).toFixed(2));
  var u=still?1:ease((tl-6.6)/4),tv=still||(tl>6.4&&tl<12.9),fa=A[f];
  for(var i=0;i<8;i++){
   var a=A[i],st=.3+i*.22,pr=still?1:ease((tl-st)/.9),lo=still?1:cl((tl-st-.5)/.45),isF=i===f;
   var op=(isF?1:1-.6*dimB)*fade;
   a.p.setAttribute('stroke-dashoffset',(1-pr).toFixed(3));a.p.setAttribute('opacity',(.6*op).toFixed(2));
   a.dot.setAttribute('opacity',(lo*op).toFixed(2));a.lb.setAttribute('opacity',(lo*(isF?1:.25+.75*(1-dimB))*fade).toFixed(2));
   var arr=isF&&tv&&u>=1;a.lb.setAttribute('class',arr?'on':'');
   a.tr.setAttribute('opacity',isF&&tv?(fade).toFixed(2):'0');if(isF)a.tr.setAttribute('stroke-dashoffset',(1-u).toFixed(3));
   if(arr){var q=still?.4:((tl-10.6)%1.6)/1.6;a.halo.setAttribute('r',(5+q*12).toFixed(1));a.halo.setAttribute('opacity',(fade*(1-q)).toFixed(2))}else a.halo.setAttribute('opacity','0');
   var po=0,pu=0;
   if(!still){
    if(tl>2&&tl<6.4&&pr>=1){pu=((tl-2)/1.5+i*.137)%1;po=Math.sin(Math.PI*pu)*sm(2,2.4,tl)*(1-sm(5.9,6.4,tl));a.pu.setAttribute('fill','#EEBF01')}
    else if(!isF&&tl>6.8&&tl<12.4){pu=1-((tl-6.8)/1.9+i*.21)%1;po=.75*Math.sin(Math.PI*pu)*sm(6.8,7.2,tl)*fade;a.pu.setAttribute('fill','#7FD6D7')}
   }
   if(po>0.01){var P=a.p.getPointAtLength(pu*a.len);a.pu.setAttribute('cx',P.x.toFixed(1));a.pu.setAttribute('cy',P.y.toFixed(1))}
   a.pu.setAttribute('opacity',po.toFixed(2));
  }
  var P0=fa.p.getPointAtLength(u*fa.len),P1=fa.p.getPointAtLength(Math.max(0,u-.02)*fa.len),P2=fa.p.getPointAtLength(Math.min(1,u+.02)*fa.len);
  var tx=P2.x-P1.x,ty=P2.y-P1.y,tn=Math.sqrt(tx*tx+ty*ty)||1;tx/=tn;ty/=tn;var nx=-ty,ny=tx;
  var vo=tv?cl((tl-6.4)/.3)*fade:0;if(still)vo=1;
  S.trav.setAttribute('cx',P0.x.toFixed(1));S.trav.setAttribute('cy',P0.y.toFixed(1));S.trav.setAttribute('opacity',vo.toFixed(2));
  var cxp,cyp;
  if(u<1){var bob=Math.sin(t*7)*1.6;cxp=P0.x+nx*10+tx*bob;cyp=P0.y+ny*10+ty*bob}
  else{var na=Math.atan2(ny,nx)+(still?0:(tl-10.6)*2.2);cxp=P0.x+Math.cos(na)*10;cyp=P0.y+Math.sin(na)*10}
  S.comp.setAttribute('cx',cxp.toFixed(1));S.comp.setAttribute('cy',cyp.toFixed(1));S.comp.setAttribute('opacity',vo.toFixed(2));
  for(k=0;k<4;k++){
   var g=S.checks[k],m=MS[k],sc=k<3?pop((u-m)/.09):pop((tl-10.6)/.35);if(still)sc=1;
   var on=tv&&(k<3?u>=m:u>=1),Q=fa.p.getPointAtLength(m*fa.len),R=fa.p.getPointAtLength(Math.max(0,m-.02)*fa.len),ex=Q.x-R.x,ey=Q.y-R.y,en=Math.sqrt(ex*ex+ey*ey)||1;
   var ox=k<3?ey/en*13:0,oy=k<3?-ex/en*13:0;if(k===3){ox=0;oy=0}
   g.setAttribute('transform','translate('+(Q.x+ox).toFixed(1)+' '+(Q.y+oy).toFixed(1)+') scale('+(on?sc:0).toFixed(2)+')');
   g.setAttribute('opacity',on?fade.toFixed(2):'0');
   if(steps[k])steps[k].classList.toggle('on',on&&fade>.5);
  }
  var p0=still||tl<6.2,p1=still||(tl>=6.2&&tl<12.6);
  if(pills[0])pills[0].classList.toggle('on',p0);if(pills[1])pills[1].classList.toggle('on',p1);
  if(chips[0])chips[0].classList.toggle('on',p0&&!still);if(chips[1])chips[1].classList.toggle('on',p1&&!still);
 }
 function tick(now){if(!run){raf=0;return}acc+=Math.min(now-last,100)/1000;last=now;render(acc);raf=requestAnimationFrame(tick)}
 function play(){if(RM||run)return;run=true;last=performance.now();if(!raf)raf=requestAnimationFrame(tick)}
 function pause(){run=false}
 build();
 if(RM){render(0,true);return}
 render(0);
 var vis=false;
 if('IntersectionObserver' in window){new IntersectionObserver(function(e){vis=e[0].isIntersecting;if(vis&&stage.clientWidth&&(stage.clientWidth<560)!==narrow){build();render(acc)}vis&&!document.hidden?play():pause()},{threshold:.15}).observe(stage)}else{vis=true;play()}
 document.addEventListener('visibilitychange',function(){document.hidden?pause():vis&&play()});
 var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){if((stage.clientWidth<560)!==narrow){build();render(acc)}},150)});
 stage.__net={seek:function(s){pause();acc=s;render(acc)},play:play,pause:pause};
}
function init(){[].forEach.call(document.querySelectorAll('.net-stage'),function(s){if(!s.__net)Net(s)})}
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init):init();
})();
