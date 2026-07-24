import{i as e}from"./preload-helper-Ct_ODC0V.js";import{B as t,D as n,G as r,H as i,K as a,R as o,Rt as s,Ut as c,V as l,Vt as u,Wt as d,Z as f,_t as p,bt as m,gt as ee,i as h,it as g,jt as _,lt as v,o as y,ot as b,r as te,rt as x,st as S,z as C}from"./iframe-DOJVC7nn.js";import{n as w,t as T}from"./CspIcon-DZSAU4sW.js";import{n as E,t as D}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as ne,t as O}from"./CspAvatar-D_h79ZkF.js";import{En as k,On as A,Sn as j,gn as re,t as M,vn as ie}from"./dist-CVsMcIYM.js";import{n as ae,t as oe}from"./CspButton-DyvV9OxJ.js";import{n as se,t as ce}from"./CspDropdownMenu-prV-Q1Tz.js";import{n as le,t as ue}from"./CspTooltip-B4UMfJ7U.js";function de(e){let t=_(!1);function n(){typeof window<`u`&&(t.value=window.innerWidth<=e)}return x(()=>{n(),window.addEventListener(`resize`,n)}),g(()=>{window.removeEventListener(`resize`,n)}),t}function fe(e){let{defaultExpanded:t=!0,persistState:n=!0}=e,r=localStorage.getItem(pe),i=_(r===null?t:r===`true`),a=de(768),s=_(!1),c=o(()=>i.value?`expanded`:`collapsed`);function l(e){i.value=e,n&&localStorage.setItem(pe,String(e))}function u(e){s.value=e}function d(){a.value?u(!s.value):l(!i.value)}function f(e){e.key===`b`&&(e.metaKey||e.ctrlKey)&&(e.preventDefault(),d())}x(()=>{window.addEventListener(`keydown`,f)}),g(()=>{window.removeEventListener(`keydown`,f)}),p(a,e=>{!e&&s.value&&(s.value=!1)});let m={state:c,isExpanded:i,isMobile:a,isMobileOpen:s,setExpanded:l,setMobileOpen:u,toggle:d};return S(ge,m),m}function N(){let e=f(ge);if(!e)throw Error(`useSidebar must be used within a CspSidebar provider`);return e}var pe,me,he,ge,P=e((()=>{n(),pe=`csp_sidebar_state`,me=`15rem`,he=`4rem`,ge=Symbol(`sidebar`),fe.__docgenInfo=Object.assign({displayName:fe.name??fe.__name},{exportName:`provideSidebar`,displayName:`provideSidebar`,type:2,props:[{name:`defaultExpanded`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`persistState`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/composables/ui/useSidebar.ts`})})),_e,ve,ye,be,xe,Se,Ce,we,Te,Ee,F,De=e((()=>{n(),M(),ae(),w(),P(),_e={class:`csp-sidebar__header`},ve={key:0,class:`csp-sidebar__brand`},ye={class:`csp-sidebar__nav`},be={key:0,class:`csp-sidebar__footer`},xe=[`data-state`,`aria-expanded`],Se={class:`csp-sidebar__header`},Ce={key:0,class:`csp-sidebar__brand`},we=[`aria-label`,`title`],Te={class:`csp-sidebar__nav`},Ee={key:0,class:`csp-sidebar__footer`},F=a({__name:`CspSidebar`,setup(e){let n=ee(),a=o(()=>!!n.logo),d=o(()=>!!n.footer),{state:f,isExpanded:p,isMobile:h,isMobileOpen:g,setMobileOpen:_,toggle:y}=N();return(e,n)=>s(h)?(b(),t(s(k),{key:0,open:s(g),"onUpdate:open":s(_)},{default:m(()=>[r(s(re),null,{default:m(()=>[r(s(ie),{class:`csp-sidebar-overlay`}),r(s(j),{class:`csp-sidebar csp-sidebar--mobile`,"aria-label":e.$attrs[`aria-label`]??`Menu de navigation`,style:c({"--sidebar-width":s(me)})},{default:m(()=>[C(`header`,_e,[a.value?(b(),i(`div`,ve,[v(e.$slots,`logo`,{},void 0,!0)])):l(``,!0),r(oe,{class:`csp-sidebar__close`,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":`Fermer le menu`,onClick:n[0]||=e=>s(_)(!1)})]),C(`nav`,ye,[v(e.$slots,`default`,{},void 0,!0)]),d.value?(b(),i(`div`,be,[v(e.$slots,`footer`,{},void 0,!0)])):l(``,!0)]),_:3},8,[`aria-label`,`style`])]),_:3})]),_:3},8,[`open`,`onUpdate:open`])):(b(),i(`nav`,{key:1,class:u([`csp-sidebar`,{"csp-sidebar--expanded":s(p)}]),"data-state":s(f),"aria-expanded":s(p),style:c({"--sidebar-width":s(me),"--sidebar-width-collapsed":s(he)})},[C(`div`,Se,[a.value&&s(p)?(b(),i(`div`,Ce,[v(e.$slots,`logo`,{},void 0,!0)])):l(``,!0),C(`button`,{type:`button`,class:`csp-sidebar__toggle`,"aria-label":s(p)?`Réduire le menu`:`Ouvrir le menu`,title:`${s(p)?`Réduire`:`Ouvrir`} (Ctrl+B)`,onClick:n[1]||=(...e)=>s(y)&&s(y)(...e)},[r(T,{name:s(p)?`ri:sidebar-fold-line`:`ri:sidebar-unfold-line`,size:18},null,8,[`name`])],8,we)]),C(`div`,Te,[v(e.$slots,`default`,{},void 0,!0)]),d.value?(b(),i(`div`,Ee,[v(e.$slots,`footer`,{},void 0,!0)])):l(``,!0)],14,xe))}})})),Oe=e((()=>{})),ke,Ae=e((()=>{De(),De(),Oe(),E(),ke=D(F,[[`__scopeId`,`data-v-40fc1d50`]]),F.__docgenInfo=Object.assign({displayName:F.name??F.__name},{exportName:`default`,displayName:`CspSidebar`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`logo`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`footer`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebar.vue`})})),je,Me,Ne,I,Pe=e((()=>{n(),P(),je=[`aria-label`],Me={key:0,class:`csp-sidebar-group__label`},Ne={class:`csp-sidebar-group__items`},I=a({__name:`CspSidebarGroup`,props:{label:{}},setup(e){let{isExpanded:t,isMobile:n}=N();return(r,a)=>(b(),i(`div`,{class:`csp-sidebar-group`,role:`group`,"aria-label":e.label},[s(t)||s(n)?(b(),i(`span`,Me,d(e.label),1)):l(``,!0),C(`div`,Ne,[v(r.$slots,`default`,{},void 0,!0)])],8,je))}})})),Fe=e((()=>{})),Ie,Le=e((()=>{Pe(),Pe(),Fe(),E(),Ie=D(I,[[`__scopeId`,`data-v-d9981547`]]),I.__docgenInfo=Object.assign({displayName:I.name??I.__name},{exportName:`default`,displayName:`CspSidebarGroup`,type:1,props:[{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`label`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarGroup.vue`})})),Re,L,ze=e((()=>{n(),M(),h(),w(),le(),P(),Re={key:0,class:`csp-sidebar-item__label`},L=a({inheritAttrs:!1,__name:`CspSidebarItem`,props:{icon:{},label:{},to:{},isActive:{type:Boolean,default:!1}},setup(e){let{isExpanded:n,isMobile:a}=N();return(o,c)=>(b(),t(ue,{content:e.label,disabled:s(n)||s(a),side:`right`,"side-offset":12},{default:m(()=>[r(s(A),{as:e.to?s(te):`button`,to:e.to,type:e.to?void 0:`button`,class:u([`csp-sidebar-item`,{"csp-sidebar-item--active":e.isActive,"csp-sidebar-item--expanded":s(n)||s(a)}]),"aria-current":e.isActive?`page`:void 0},{default:m(()=>[r(T,{class:`csp-sidebar-item__icon`,name:e.icon,size:16},null,8,[`name`]),s(n)||s(a)?(b(),i(`span`,Re,d(e.label),1)):l(``,!0)]),_:1},8,[`as`,`to`,`type`,`class`,`aria-current`])]),_:1},8,[`content`,`disabled`]))}})})),Be=e((()=>{})),Ve,He=e((()=>{ze(),ze(),Be(),E(),Ve=D(L,[[`__scopeId`,`data-v-d69b2512`]]),L.__docgenInfo=Object.assign({displayName:L.name??L.__name},{exportName:`default`,displayName:`CspSidebarItem`,type:1,props:[{name:`icon`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`to`,global:!1,description:``,tags:[],required:!1,type:`any`,declarations:[],schema:`any`},{name:`isActive`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`isActive`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`icon`,type:`string`,description:``,declarations:[],schema:`string`},{name:`to`,type:`any`,description:``,declarations:[],schema:`any`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarItem.vue`})})),Ue,We,R,Ge=e((()=>{n(),P(),Ue={class:`csp-sidebar-logo`},We={key:0,class:`csp-sidebar-logo__subtitle`},R=a({__name:`CspSidebarLogo`,setup(e){let{isExpanded:t,isMobile:n}=N();return(e,r)=>(b(),i(`div`,Ue,[r[0]||=C(`span`,{class:`csp-sidebar-logo__title`},`CSPLab`,-1),s(t)||s(n)?(b(),i(`span`,We,` ATS `)):l(``,!0)]))}})})),Ke=e((()=>{})),qe,Je=e((()=>{Ge(),Ge(),Ke(),E(),qe=D(R,[[`__scopeId`,`data-v-8492f1ff`]]),R.__docgenInfo=Object.assign({displayName:R.name??R.__name},{exportName:`default`,displayName:`CspSidebarLogo`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarLogo.vue`})})),z,Ye=e((()=>{n(),P(),z=a({__name:`CspSidebarProvider`,props:{defaultExpanded:{type:Boolean,default:!0},persistState:{type:Boolean,default:!0}},setup(e){let t=e;return fe({defaultExpanded:t.defaultExpanded,persistState:t.persistState}),(e,t)=>v(e.$slots,`default`)}})})),Xe,Ze=e((()=>{Ye(),Ye(),Xe=z,z.__docgenInfo=Object.assign({displayName:z.name??z.__name},{exportName:`default`,displayName:`CspSidebarProvider`,type:1,props:[{name:`defaultExpanded`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`persistState`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`defaultExpanded`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`persistState`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarProvider.vue`})})),B,Qe=e((()=>{n(),ae(),P(),B=a({__name:`CspSidebarTrigger`,setup(e){let{toggle:n,isMobile:r}=N();return(e,i)=>s(r)?(b(),t(oe,{key:0,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:menu-line`,"aria-label":`Ouvrir le menu`,onClick:s(n)},null,8,[`onClick`])):l(``,!0)}})})),$e,et=e((()=>{Qe(),Qe(),$e=B,B.__docgenInfo=Object.assign({displayName:B.name??B.__name},{exportName:`default`,displayName:`CspSidebarTrigger`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarTrigger.vue`})}));function tt(){return Math.random().toString(36).slice(2,11)}function nt(e){let{baseUrl:t=``,Request:n=globalThis.Request,fetch:r=globalThis.fetch,querySerializer:i,bodySerializer:a,pathSerializer:o,headers:s,requestInitExt:c=void 0,...l}={...e};c=ft()?c:void 0,t=ut(t);let u=[];async function d(e,d){let{baseUrl:f,fetch:p=r,Request:m=n,headers:ee,params:h={},parseAs:g=`json`,querySerializer:_,bodySerializer:v=a??st,pathSerializer:y,body:b,middleware:te=[],...x}=d||{},S=t;f&&(S=ut(f)??t);let C=typeof i==`function`?i:at(i);_&&(C=typeof _==`function`?_:at({...typeof i==`object`?i:{},..._}));let w=y||o||ot,T=b===void 0?void 0:v(b,lt(s,ee,h.header)),E=lt(T===void 0||T instanceof FormData?{}:{"Content-Type":`application/json`},s,ee,h.header),D=[...u,...te],ne={redirect:`follow`,...l,...x,body:T,headers:E},O,k,A=new m(ct(e,{baseUrl:S,params:h,querySerializer:C,pathSerializer:w}),ne),j;for(let e in x)e in A||(A[e]=x[e]);if(D.length){O=tt(),k=Object.freeze({baseUrl:S,fetch:p,parseAs:g,querySerializer:C,bodySerializer:v,pathSerializer:w});for(let t of D)if(t&&typeof t==`object`&&typeof t.onRequest==`function`){let n=await t.onRequest({request:A,schemaPath:e,params:h,options:k,id:O});if(n)if(n instanceof m)A=n;else if(n instanceof Response){j=n;break}else throw Error(`onRequest: must return new Request() or Response() when modifying the request`)}}if(!j){try{j=await p(A,c)}catch(t){let n=t;if(D.length)for(let t=D.length-1;t>=0;t--){let r=D[t];if(r&&typeof r==`object`&&typeof r.onError==`function`){let t=await r.onError({request:A,error:n,schemaPath:e,params:h,options:k,id:O});if(t){if(t instanceof Response){n=void 0,j=t;break}if(t instanceof Error){n=t;continue}throw Error(`onError: must return new Response() or instance of Error`)}}}if(n)throw n}if(D.length)for(let t=D.length-1;t>=0;t--){let n=D[t];if(n&&typeof n==`object`&&typeof n.onResponse==`function`){let t=await n.onResponse({request:A,response:j,schemaPath:e,params:h,options:k,id:O});if(t){if(!(t instanceof Response))throw Error(`onResponse: must return new Response() when modifying the response`);j=t}}}}let re=j.headers.get(`Content-Length`);if(j.status===204||A.method===`HEAD`||re===`0`&&!j.headers.get(`Transfer-Encoding`)?.includes(`chunked`))return j.ok?{data:void 0,response:j}:{error:void 0,response:j};if(j.ok)return{data:await(async()=>{if(g===`stream`)return j.body;if(g===`json`&&!re){let e=await j.text();return e?JSON.parse(e):void 0}return await j[g]()})(),response:j};let M=await j.text();try{M=JSON.parse(M)}catch{}return{error:M,response:j}}return{request(e,t,n){return d(t,{...n,method:e.toUpperCase()})},GET(e,t){return d(e,{...t,method:`GET`})},PUT(e,t){return d(e,{...t,method:`PUT`})},POST(e,t){return d(e,{...t,method:`POST`})},DELETE(e,t){return d(e,{...t,method:`DELETE`})},OPTIONS(e,t){return d(e,{...t,method:`OPTIONS`})},HEAD(e,t){return d(e,{...t,method:`HEAD`})},PATCH(e,t){return d(e,{...t,method:`PATCH`})},TRACE(e,t){return d(e,{...t,method:`TRACE`})},use(...e){for(let t of e)if(t){if(typeof t!=`object`||!(`onRequest`in t||`onResponse`in t||`onError`in t))throw Error("Middleware must be an object with one of `onRequest()`, `onResponse() or `onError()`");u.push(t)}},eject(...e){for(let t of e){let e=u.indexOf(t);e!==-1&&u.splice(e,1)}}}}function V(e,t,n){if(t==null)return``;if(typeof t==`object`)throw Error("Deeply-nested arrays/objects aren’t supported. Provide your own `querySerializer()` to handle these.");return`${e}=${n?.allowReserved===!0?t:encodeURIComponent(t)}`}function rt(e,t,n){if(!t||typeof t!=`object`)return``;let r=[],i={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`;if(n.style!==`deepObject`&&n.explode===!1){for(let e in t)r.push(e,n.allowReserved===!0?t[e]:encodeURIComponent(t[e]));let i=r.join(`,`);switch(n.style){case`form`:return`${e}=${i}`;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return i}}for(let i in t){let a=n.style===`deepObject`?`${e}[${i}]`:i;r.push(V(a,t[i],n))}let a=r.join(i);return n.style===`label`||n.style===`matrix`?`${i}${a}`:a}function it(e,t,n){if(!Array.isArray(t))return``;if(n.explode===!1){let r={form:`,`,spaceDelimited:`%20`,pipeDelimited:`|`}[n.style]||`,`,i=(n.allowReserved===!0?t:t.map(e=>encodeURIComponent(e))).join(r);switch(n.style){case`simple`:return i;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return`${e}=${i}`}}let r={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`,i=[];for(let r of t)n.style===`simple`||n.style===`label`?i.push(n.allowReserved===!0?r:encodeURIComponent(r)):i.push(V(e,r,n));return n.style===`label`||n.style===`matrix`?`${r}${i.join(r)}`:i.join(r)}function at(e){return function(t){let n=[];if(t&&typeof t==`object`)for(let r in t){let i=t[r];if(i!=null){if(Array.isArray(i)){if(i.length===0)continue;n.push(it(r,i,{style:`form`,explode:!0,...e?.array,allowReserved:e?.allowReserved||!1}));continue}if(typeof i==`object`){n.push(rt(r,i,{style:`deepObject`,explode:!0,...e?.object,allowReserved:e?.allowReserved||!1}));continue}n.push(V(r,i,e))}}return n.join(`&`)}}function ot(e,t){let n=e;for(let r of e.match(dt)??[]){let e=r.substring(1,r.length-1),i=!1,a=`simple`;if(e.endsWith(`*`)&&(i=!0,e=e.substring(0,e.length-1)),e.startsWith(`.`)?(a=`label`,e=e.substring(1)):e.startsWith(`;`)&&(a=`matrix`,e=e.substring(1)),!t||t[e]===void 0||t[e]===null)continue;let o=t[e];if(Array.isArray(o)){n=n.replace(r,it(e,o,{style:a,explode:i}));continue}if(typeof o==`object`){n=n.replace(r,rt(e,o,{style:a,explode:i}));continue}if(a===`matrix`){n=n.replace(r,`;${V(e,o)}`);continue}n=n.replace(r,a===`label`?`.${encodeURIComponent(o)}`:encodeURIComponent(o))}return n}function st(e,t){return e instanceof FormData?e:t&&(t.get instanceof Function?t.get(`Content-Type`)??t.get(`content-type`):t[`Content-Type`]??t[`content-type`])===`application/x-www-form-urlencoded`?new URLSearchParams(e).toString():JSON.stringify(e)}function ct(e,t){let n=`${t.baseUrl}${e}`;t.params?.path&&(n=t.pathSerializer(n,t.params.path));let r=t.querySerializer(t.params.query??{});return r.startsWith(`?`)&&(r=r.substring(1)),r&&(n+=`?${r}`),n}function lt(...e){let t=new Headers;for(let n of e){if(!n||typeof n!=`object`)continue;let e=n instanceof Headers?n.entries():Object.entries(n);for(let[n,r]of e)if(r===null)t.delete(n);else if(Array.isArray(r))for(let e of r)t.append(n,e);else r!==void 0&&t.set(n,r)}return t}function ut(e){return e.endsWith(`/`)?e.substring(0,e.length-1):e}var dt,ft,pt=e((()=>{dt=/\{[^{}]+\}/g,ft=()=>typeof process==`object`&&Number.parseInt(process?.versions?.node?.substring(0,2))>=18&&process.versions.undici}));function mt(e){if(!e||typeof e!=`object`||Array.isArray(e))return{};let t=e,n=t.status===`error`&&t.details&&typeof t.details==`object`&&!Array.isArray(t.details)?t.details:t,r={};for(let[e,i]of Object.entries(n))if(!(n===t&&_t.has(e)))if(Array.isArray(i)){let t=i.filter(e=>typeof e==`string`);t.length>0&&(r[e]=t)}else typeof i==`string`&&(r[e]=[i]);return r}var H,ht,gt,_t,vt=e((()=>{H=class extends Error{status;statusText;data;constructor(e,t,n){super(`HTTP ${e}: ${t}`),this.status=e,this.statusText=t,this.data=n,this.name=`HttpError`}},ht=class extends Error{cause;constructor(e){super(`Network request failed`),this.cause=e,this.name=`NetworkError`}},gt=class extends H{fieldErrors;constructor(e,t,n,r){super(e,t,n),this.fieldErrors=r,this.name=`ValidationError`}},_t=new Set([`detail`,`status`,`message`,`type`])}));function yt(){let e=document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);return e?decodeURIComponent(e[1]):``}function bt(){let e=encodeURIComponent(window.location.pathname+window.location.search);throw window.location.href=`/utilisateur/connexion?next=${e}`,Error(`Redirecting to login`)}function xt(e){let t=[`GET`,`POST`,`PUT`,`PATCH`,`DELETE`,`HEAD`,`OPTIONS`,`TRACE`],n={...e};for(let r of t){let t=e[r];n[r]=async(...e)=>{try{return await t(...e)}catch(e){throw e instanceof DOMException&&e.name===`AbortError`||e instanceof H||e instanceof Error&&e.message===`Redirecting to login`?e:new ht(e)}}}return n}var St,Ct,U,wt=e((()=>{pt(),vt(),St={async onRequest({request:e}){if(e.method!==`GET`)return e.headers.set(`X-CSRFToken`,yt()),e}},Ct={async onResponse({response:e}){if(e.ok)return;e.status===401&&bt();let t=await e.clone().json().catch(()=>void 0);throw e.status===400||e.status===422?new gt(e.status,e.statusText,t,mt(t)):new H(e.status,e.statusText,t)}},U=nt({baseUrl:typeof window<`u`?window.location.origin:``,credentials:`same-origin`,fetch:(...e)=>globalThis.fetch(...e)}),U.use(St),U.use(Ct),xt(U)}));async function Tt(){await fetch(`/utilisateur/deconnexion`,{method:`POST`,credentials:`same-origin`,headers:{"X-CSRFToken":yt()}}),window.location.href=`/`}var Et=e((()=>{wt()}));function Dt(){return typeof window>`u`?!1:window.matchMedia(`(prefers-color-scheme: dark)`).matches}function W(e){typeof document>`u`||document.documentElement.setAttribute(`data-fr-theme`,e?`dark`:`light`)}function Ot(){let e=o(()=>G.value===`system`?K.value:G.value===`dark`);function t(t){G.value=t,localStorage.setItem(kt,t),W(e.value)}function n(){t(e.value?`light`:`dark`)}let r=null,i=null;return x(()=>{K.value=Dt();let t=localStorage.getItem(kt);t&&[`light`,`dark`,`system`].includes(t)&&(G.value=t),W(e.value),r=window.matchMedia(`(prefers-color-scheme: dark)`),i=e=>{K.value=e.matches,G.value===`system`&&W(e.matches)},r.addEventListener(`change`,i)}),g(()=>{r&&i&&r.removeEventListener(`change`,i)}),p(e,e=>{W(e)}),{colorMode:G,isDark:e,setColorMode:t,toggle:n}}var kt,G,K,At=e((()=>{n(),kt=`csp_color_mode`,G=_(`system`),K=_(!1)})),jt,Mt,Nt,q,Pt=e((()=>{n(),Et(),ne(),se(),w(),At(),P(),jt={key:0,class:`csp-sidebar-user__info`},Mt={class:`csp-sidebar-user__name`},Nt={key:0,class:`csp-sidebar-user__role`},q=a({__name:`CspSidebarUser`,props:{name:{},role:{}},setup(e){let{isExpanded:n,isMobile:a}=N(),{isDark:o,toggle:c}=Ot();return(f,p)=>(b(),t(ce,{side:`right`,align:`end`,sections:[{items:[{label:s(o)?`Mode clair`:`Mode sombre`,icon:s(o)?`ri:sun-line`:`ri:moon-line`,onSelect:s(c)}]},{items:[{label:`Mon profil`,icon:`ri:user-line`},{label:`Paramètres`,icon:`ri:settings-3-line`}]},{items:[{label:`Se déconnecter`,icon:`ri:logout-box-r-line`,destructive:!0,onSelect:s(Tt)}]}]},{trigger:m(()=>[C(`button`,{type:`button`,class:u([`csp-sidebar-user`,{"csp-sidebar-user--expanded":s(n)||s(a)}])},[r(O,{name:e.name,size:`md`},null,8,[`name`]),s(n)||s(a)?(b(),i(`div`,jt,[C(`span`,Mt,d(e.name),1),e.role?(b(),i(`span`,Nt,d(e.role),1)):l(``,!0)])):l(``,!0),s(n)||s(a)?(b(),t(T,{key:1,name:`ri:expand-up-down-line`,size:16,class:`csp-sidebar-user__chevron`})):l(``,!0)],2)]),_:1},8,[`sections`]))}})})),Ft=e((()=>{})),It,Lt=e((()=>{Pt(),Pt(),Ft(),E(),It=D(q,[[`__scopeId`,`data-v-eb144a6d`]]),q.__docgenInfo=Object.assign({displayName:q.name??q.__name},{exportName:`default`,displayName:`CspSidebarUser`,type:1,props:[{name:`name`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`role`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`name`,type:`string`,description:``,declarations:[],schema:`string`},{name:`role`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarUser.vue`})})),Rt,J,Y,X,Z,Q,$,zt;e((()=>{h(),Ae(),Le(),He(),Je(),Ze(),et(),Lt(),Rt={title:`Compositions/Génériques/CspSidebar`,component:Xe,parameters:{layout:`fullscreen`,docs:{description:{component:'\nSidebar de navigation adaptée au DSFR.\n\n## Composants\n\n- `CspSidebarProvider` : contexte partagé (état, mobile, raccourcis)\n- `CspSidebar` : panneau de navigation\n- `CspSidebarTrigger` : bouton hamburger mobile (dans le header)\n- `CspSidebarGroup`, `CspSidebarItem`, `CspSidebarLogo`, `CspSidebarUser`\n\n## Usage\n\n```vue\n<CspAppShell :navigation="navigation">\n  <!-- contenu de page -->\n</CspAppShell>\n```\n        '}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},J=`
  <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
    <div style="display: flex; min-height: 100vh;">
      <aside style="flex-shrink: 0; border-right: 1px solid var(--border-default-grey);">
        <CspSidebar>
          <template #logo>
            <CspSidebarLogo />
          </template>

          <CspSidebarGroup label="Groupe A">
            <CspSidebarItem icon="ri:dashboard-line" label="Première entrée" :to="{ path: '/premiere' }" />
            <CspSidebarItem icon="ri:briefcase-line" label="Entrée active" :to="{ path: '/active' }" :is-active="true" />
          </CspSidebarGroup>

          <CspSidebarGroup label="Groupe B">
            <CspSidebarItem icon="ri:group-line" label="Troisième entrée" :to="{ path: '/troisieme' }" />
            <CspSidebarItem icon="ri:layout-column-line" label="Quatrième entrée" :to="{ path: '/quatrieme' }" />
          </CspSidebarGroup>

          <CspSidebarGroup label="Groupe C">
            <CspSidebarItem icon="ri:settings-3-line" label="Cinquième entrée" :to="{ path: '/cinquieme' }" />
          </CspSidebarGroup>

          <template #footer>
            <CspSidebarUser name="Prénom Nom" role="Rôle" />
          </template>
        </CspSidebar>
      </aside>

      <div style="flex: 1; min-width: 0;">
        <header style="display: flex; padding: 0.75rem 1rem; border-bottom: 1px solid var(--border-default-grey);">
          <CspSidebarTrigger />
        </header>

        <div style="padding: 2rem; max-width: 800px;">
          <h1 style="margin: 0 0 0.5rem; font-size: 1.5rem; font-weight: 600; color: var(--text-title-grey);">
            Contenu
          </h1>
          <p style="color: var(--text-mention-grey); margin: 0 0 1rem;">
            Utilisez <kbd style="padding: 0.125rem 0.375rem; border-radius: 0.25rem; background: var(--background-contrast-grey); font-family: monospace; font-size: 0.75rem;">Ctrl+B</kbd> pour toggle la sidebar.
          </p>
          <p style="color: var(--text-mention-grey); margin: 0;">
            En mode collapsed, survolez les icônes pour voir les tooltips.
          </p>
        </div>
      </div>
    </div>
  </CspSidebarProvider>
`,Y={CspSidebar:ke,CspSidebarGroup:Ie,CspSidebarItem:Ve,CspSidebarLogo:qe,CspSidebarProvider:Xe,CspSidebarTrigger:$e,CspSidebarUser:It},X={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Z={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Q={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},$={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:Y,setup(){let t=y();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
      <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
        <div style="display: flex; min-height: 100vh;">
          <aside style="flex-shrink: 0; border-right: 1px solid var(--border-default-grey);">
            <CspSidebar>
              <template #logo>
                <CspSidebarLogo />
              </template>

              <CspSidebarGroup label="Navigation">
                <CspSidebarItem
                  v-for="item in items"
                  :key="item.to"
                  :icon="item.icon"
                  :label="item.label"
                  :to="item.to"
                  :is-active="route.path === item.to"
                />
              </CspSidebarGroup>
            </CspSidebar>
          </aside>

          <div style="flex: 1; min-width: 0;">
            <header style="display: flex; padding: 0.75rem 1rem; border-bottom: 1px solid var(--border-default-grey);">
              <CspSidebarTrigger />
            </header>

            <div style="padding: 2rem;">
              <p style="color: var(--text-mention-grey); margin: 0;">
                Cliquez une entrée pour naviguer. Route active :
                <code style="padding: 0.125rem 0.375rem; border-radius: 0.25rem; background: var(--background-contrast-grey); font-family: monospace;">{{ route.path }}</code>
              </p>
            </div>
          </div>
        </div>
      </CspSidebarProvider>
    `})},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  args: {
    defaultExpanded: true,
    persistState: false
  },
  render: args => ({
    components,
    setup: () => ({
      defaultExpanded: args.defaultExpanded,
      persistState: args.persistState
    }),
    template: sidebarTemplate
  })
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  args: {
    defaultExpanded: false,
    persistState: false
  },
  render: args => ({
    components,
    setup: () => ({
      defaultExpanded: args.defaultExpanded,
      persistState: args.persistState
    }),
    template: sidebarTemplate
  })
}`,...Z.parameters?.docs?.source}}},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
  args: {
    defaultExpanded: true,
    persistState: false
  },
  parameters: {
    viewport: {
      defaultViewport: 'mobile1'
    }
  },
  render: args => ({
    components,
    setup: () => ({
      defaultExpanded: args.defaultExpanded,
      persistState: args.persistState
    }),
    template: sidebarTemplate
  })
}`,...Q.parameters?.docs?.source}}},$.parameters={...$.parameters,docs:{...$.parameters?.docs,source:{originalSource:`{
  name: 'Avec liens de navigation',
  args: {
    defaultExpanded: true,
    persistState: false
  },
  parameters: {
    docs: {
      description: {
        story: 'Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l\\'état actif en direct. Permet de tester les états actif / inactif sans câbler \`is-active\` à la main.'
      }
    }
  },
  render: args => ({
    components,
    setup() {
      const route = useRoute();
      const items = [{
        icon: 'ri:dashboard-line',
        label: 'Première entrée',
        to: '/premiere'
      }, {
        icon: 'ri:briefcase-line',
        label: 'Deuxième entrée',
        to: '/deuxieme'
      }, {
        icon: 'ri:group-line',
        label: 'Troisième entrée',
        to: '/troisieme'
      }, {
        icon: 'ri:settings-3-line',
        label: 'Quatrième entrée',
        to: '/quatrieme'
      }];
      return {
        defaultExpanded: args.defaultExpanded,
        persistState: args.persistState,
        route,
        items
      };
    },
    template: \`
      <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
        <div style="display: flex; min-height: 100vh;">
          <aside style="flex-shrink: 0; border-right: 1px solid var(--border-default-grey);">
            <CspSidebar>
              <template #logo>
                <CspSidebarLogo />
              </template>

              <CspSidebarGroup label="Navigation">
                <CspSidebarItem
                  v-for="item in items"
                  :key="item.to"
                  :icon="item.icon"
                  :label="item.label"
                  :to="item.to"
                  :is-active="route.path === item.to"
                />
              </CspSidebarGroup>
            </CspSidebar>
          </aside>

          <div style="flex: 1; min-width: 0;">
            <header style="display: flex; padding: 0.75rem 1rem; border-bottom: 1px solid var(--border-default-grey);">
              <CspSidebarTrigger />
            </header>

            <div style="padding: 2rem;">
              <p style="color: var(--text-mention-grey); margin: 0;">
                Cliquez une entrée pour naviguer. Route active :
                <code style="padding: 0.125rem 0.375rem; border-radius: 0.25rem; background: var(--background-contrast-grey); font-family: monospace;">{{ route.path }}</code>
              </p>
            </div>
          </div>
        </div>
      </CspSidebarProvider>
    \`
  })
}`,...$.parameters?.docs?.source}}},zt=[`Default`,`Collapsed`,`Mobile`,`WithRouterLinks`]}))();export{Z as Collapsed,X as Default,Q as Mobile,$ as WithRouterLinks,zt as __namedExportsOrder,Rt as default};