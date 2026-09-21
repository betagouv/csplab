import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,B as n,C as r,D as i,Dt as a,G as o,H as s,N as c,O as l,Ot as u,Q as d,S as f,St as p,Tt as m,U as h,a as g,b as _,c as v,ht as y,i as ee,rt as b,s as te,w as x,x as S,z as C}from"./iframe-Bd_sG6wG.js";import{n as w,t as T}from"./CspIcon-BgVOFeVS.js";import{n as E,t as D}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as ne,t as O}from"./CspAvatar-BxBHi7zF.js";import{n as k,t as A}from"./Primitive-DwhLlyip.js";import{n as j,t as M}from"./CspDropdownMenu-3u2S4cIA.js";import{n as N,t as re}from"./CspTooltip-CySMFnJy.js";import{a as ie,c as ae,i as oe,n as se,o as ce,r as le,s as ue,t as de}from"./DialogPortal-BpmyvdJC.js";import{n as fe,t as pe}from"./CspButton-By-ovnsp.js";import{n as me,r as he}from"./breakpoints-DCpfEkNF.js";function ge(e){let t=y(!1),r;function i(){t.value=r?.matches??!1}return C(()=>{r=window.matchMedia(e),i(),r.addEventListener(`change`,i)}),n(()=>{r?.removeEventListener(`change`,i)}),t}function _e(){return(_e=e((()=>{v()})))()}function ve(e){let{defaultExpanded:r=!0,persistState:i=!0}=e,a=localStorage.getItem(F),o=y(a===null?r:a===`true`),s=ge(me(`md`)),c=y(!1),l=_(()=>o.value?`expanded`:`collapsed`);function u(e){o.value=e,i&&localStorage.setItem(F,String(e))}function d(e){c.value=e}function f(){s.value?d(!c.value):u(!o.value)}function p(e){e.key===`b`&&(e.metaKey||e.ctrlKey)&&(e.preventDefault(),f())}C(()=>{window.addEventListener(`keydown`,p)}),n(()=>{window.removeEventListener(`keydown`,p)}),t(s,e=>{!e&&c.value&&(c.value=!1)});let m={state:l,isExpanded:o,isMobile:s,isMobileOpen:c,setExpanded:u,setMobileOpen:d,toggle:f};return h(L,m),m}function P(){let e=c(L);if(!e)throw Error(`useSidebar must be used within a CspSidebar provider`);return e}var F,I,ye,L;function R(){return(R=e((()=>{v(),he(),_e(),F=`csp_sidebar_state`,I=`15rem`,ye=`4rem`,L=Symbol(`sidebar`)})))()}var be,xe,Se,Ce,we,Te,Ee,De,Oe,ke,Ae;function je(){return(je=e((()=>{v(),ce(),oe(),se(),ae(),fe(),w(),R(),be={class:`csp-sidebar__header`},xe={key:0,class:`csp-sidebar__brand`},Se={class:`csp-sidebar__nav`},Ce={key:0,class:`csp-sidebar__footer`},we=[`data-state`,`aria-expanded`],Te={class:`csp-sidebar__header`},Ee={key:0,class:`csp-sidebar__brand`},De=[`aria-label`,`title`],Oe={class:`csp-sidebar__nav`},ke={key:0,class:`csp-sidebar__footer`},Ae=l({__name:`CspSidebar`,setup(e){let t=d(),n=_(()=>!!t.logo),c=_(()=>!!t.footer),{state:l,isExpanded:u,isMobile:h,isMobileOpen:g,setMobileOpen:v,toggle:y}=P();return(e,t)=>p(h)?(s(),f(p(ue),{key:0,open:p(g),"onUpdate:open":p(v)},{default:b(()=>[i(p(de),null,{default:b(()=>[i(p(le),{class:`csp-sidebar-overlay`}),i(p(ie),{class:`csp-sidebar csp-sidebar--mobile`,"aria-label":e.$attrs[`aria-label`]??`Menu de navigation`,style:a({"--sidebar-width":p(I)})},{default:b(()=>[S(`header`,be,[n.value?(s(),x(`div`,xe,[o(e.$slots,`logo`,{},void 0,!0)])):r(``,!0),i(pe,{class:`csp-sidebar__close`,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":`Fermer le menu`,onClick:t[0]||=e=>p(v)(!1)})]),S(`nav`,Se,[o(e.$slots,`default`,{},void 0,!0)]),c.value?(s(),x(`div`,Ce,[o(e.$slots,`footer`,{},void 0,!0)])):r(``,!0)]),_:3},8,[`aria-label`,`style`])]),_:3})]),_:3},8,[`open`,`onUpdate:open`])):(s(),x(`nav`,{key:1,class:m([`csp-sidebar`,{"csp-sidebar--expanded":p(u)}]),"data-state":p(l),"aria-expanded":p(u),style:a({"--sidebar-width":p(I),"--sidebar-width-collapsed":p(ye)})},[S(`div`,Te,[n.value&&p(u)?(s(),x(`div`,Ee,[o(e.$slots,`logo`,{},void 0,!0)])):r(``,!0),S(`button`,{type:`button`,class:`csp-sidebar__toggle`,"aria-label":p(u)?`Réduire le menu`:`Ouvrir le menu`,title:`${p(u)?`Réduire`:`Ouvrir`} (Ctrl+B)`,onClick:t[1]||=(...e)=>p(y)&&p(y)(...e)},[i(T,{name:p(u)?`ri:sidebar-fold-line`:`ri:sidebar-unfold-line`,size:18},null,8,[`name`])],8,De)]),S(`div`,Oe,[o(e.$slots,`default`,{},void 0,!0)]),c.value?(s(),x(`div`,ke,[o(e.$slots,`footer`,{},void 0,!0)])):r(``,!0)],14,we))}})})))()}var Me;function Ne(){return(Ne=e((()=>{je(),E(),Me=D(Ae,[[`__scopeId`,`data-v-40fc1d50`]])})))()}function Pe(e,t){return s(),x(`div`,Fe,[S(`div`,Ie,[o(e.$slots,`default`,{},void 0,!0)])])}var z,Fe,Ie,Le;function Re(){return(Re=e((()=>{v(),E(),z={},Fe={class:`csp-sidebar-group`},Ie={class:`csp-sidebar-group__items`},Le=D(z,[[`render`,Pe],[`__scopeId`,`data-v-a36d535a`]]),z.__docgenInfo=Object.assign({displayName:z.name??z.__name},{exportName:`default`,displayName:`CspSidebarGroup`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey`,schema:`PropertyKey`,declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef`,schema:`VNodeRef`,declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean`,schema:`boolean`,declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string`,schema:`string`,declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[]`,schema:`VNodeUpdateHook | VNodeUpdateHook[]`,declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[]`,schema:`VNodeUpdateHook | VNodeUpdateHook[]`,declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[{name:`default`,type:`{}`,description:``,tags:[],schema:`{}`,declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarGroup.vue`})})))()}var ze,Be;function Ve(){return(Ve=e((()=>{v(),k(),g(),w(),N(),R(),ze={key:0,class:`csp-sidebar-item__label`},Be=l({inheritAttrs:!1,__name:`CspSidebarItem`,props:{icon:{},label:{},to:{},isActive:{type:Boolean,default:!1}},setup(e){let{isExpanded:t,isMobile:n}=P();return(a,o)=>(s(),f(re,{content:e.label,disabled:p(t)||p(n),side:`right`,"side-offset":12},{default:b(()=>[i(p(A),{as:e.to?p(ee):`button`,to:e.to,type:e.to?void 0:`button`,class:m([`csp-sidebar-item`,{"csp-sidebar-item--active":e.isActive,"csp-sidebar-item--expanded":p(t)||p(n)}]),"aria-current":e.isActive?`page`:void 0},{default:b(()=>[i(T,{class:`csp-sidebar-item__icon`,name:e.icon,size:16},null,8,[`name`]),p(t)||p(n)?(s(),x(`span`,ze,u(e.label),1)):r(``,!0)]),_:1},8,[`as`,`to`,`type`,`class`,`aria-current`])]),_:1},8,[`content`,`disabled`]))}})})))()}var He;function Ue(){return(Ue=e((()=>{Ve(),E(),He=D(Be,[[`__scopeId`,`data-v-d69b2512`]])})))()}var We,Ge,Ke;function qe(){return(qe=e((()=>{v(),R(),We={class:`csp-sidebar-logo`},Ge={key:0,class:`csp-sidebar-logo__subtitle`},Ke=l({__name:`CspSidebarLogo`,setup(e){let{isExpanded:t,isMobile:n}=P();return(e,i)=>(s(),x(`div`,We,[i[0]||=S(`span`,{class:`csp-sidebar-logo__title`},`CSPLab`,-1),p(t)||p(n)?(s(),x(`span`,Ge,` ATS `)):r(``,!0)]))}})})))()}var Je;function Ye(){return(Ye=e((()=>{qe(),E(),Je=D(Ke,[[`__scopeId`,`data-v-8492f1ff`]])})))()}var Xe;function Ze(){return(Ze=e((()=>{v(),R(),Xe=l({__name:`CspSidebarProvider`,props:{defaultExpanded:{type:Boolean,default:!0},persistState:{type:Boolean,default:!0}},setup(e){let t=e;return ve({defaultExpanded:t.defaultExpanded,persistState:t.persistState}),(e,t)=>o(e.$slots,`default`)}})})))()}var B;function Qe(){return(Qe=e((()=>{Ze(),B=Xe})))()}var $e;function et(){return(et=e((()=>{v(),fe(),R(),$e=l({__name:`CspSidebarTrigger`,setup(e){let{toggle:t,isMobile:n}=P();return(e,i)=>p(n)?(s(),f(pe,{key:0,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:menu-line`,"aria-label":`Ouvrir le menu`,onClick:p(t)},null,8,[`onClick`])):r(``,!0)}})})))()}var tt;function nt(){return(nt=e((()=>{et(),tt=$e})))()}function rt(){return Math.random().toString(36).slice(2,11)}function it(e){let{baseUrl:t=``,Request:n=globalThis.Request,fetch:r=globalThis.fetch,querySerializer:i,bodySerializer:a,pathSerializer:o,headers:s,requestInitExt:c=void 0,...l}={...e};c=mt()?c:void 0,t=ft(t);let u=[];async function d(e,d){let{baseUrl:f,fetch:p=r,Request:m=n,headers:h,params:g={},parseAs:_=`json`,querySerializer:v,bodySerializer:y=a??lt,pathSerializer:ee,body:b,middleware:te=[],...x}=d||{},S=t;f&&(S=ft(f)??t);let C=typeof i==`function`?i:st(i);v&&(C=typeof v==`function`?v:st({...typeof i==`object`?i:{},...v}));let w=ee||o||ct,T=b===void 0?void 0:y(b,dt(s,h,g.header)),E=dt(T===void 0||T instanceof FormData?{}:{"Content-Type":`application/json`},s,h,g.header),D=[...u,...te],ne={redirect:`follow`,...l,...x,body:T,headers:E},O,k,A=new m(ut(e,{baseUrl:S,params:g,querySerializer:C,pathSerializer:w}),ne),j;for(let e in x)e in A||(A[e]=x[e]);if(D.length){O=rt(),k=Object.freeze({baseUrl:S,fetch:p,parseAs:_,querySerializer:C,bodySerializer:y,pathSerializer:w});for(let t of D)if(t&&typeof t==`object`&&typeof t.onRequest==`function`){let n=await t.onRequest({request:A,schemaPath:e,params:g,options:k,id:O});if(n){if(n instanceof m)A=n;else if(n instanceof Response){j=n;break}else throw Error(`onRequest: must return new Request() or Response() when modifying the request`)}}}if(!j){try{j=await p(A,c)}catch(t){let n=t;if(D.length)for(let t=D.length-1;t>=0;t--){let r=D[t];if(r&&typeof r==`object`&&typeof r.onError==`function`){let t=await r.onError({request:A,error:n,schemaPath:e,params:g,options:k,id:O});if(t){if(t instanceof Response){n=void 0,j=t;break}if(t instanceof Error){n=t;continue}throw Error(`onError: must return new Response() or instance of Error`)}}}if(n)throw n}if(D.length)for(let t=D.length-1;t>=0;t--){let n=D[t];if(n&&typeof n==`object`&&typeof n.onResponse==`function`){let t=await n.onResponse({request:A,response:j,schemaPath:e,params:g,options:k,id:O});if(t){if(!(t instanceof Response))throw Error(`onResponse: must return new Response() when modifying the response`);j=t}}}}let M=j.headers.get(`Content-Length`);if(j.status===204||A.method===`HEAD`||M===`0`&&!j.headers.get(`Transfer-Encoding`)?.includes(`chunked`))return j.ok?{data:void 0,response:j}:{error:void 0,response:j};if(j.ok)return{data:await(async()=>{if(_===`stream`)return j.body;if(_===`json`&&!M){let e=await j.text();return e?JSON.parse(e):void 0}return await j[_]()})(),response:j};let N=await j.text();try{N=JSON.parse(N)}catch{}return{error:N,response:j}}return{request(e,t,n){return d(t,{...n,method:e.toUpperCase()})},GET(e,t){return d(e,{...t,method:`GET`})},PUT(e,t){return d(e,{...t,method:`PUT`})},POST(e,t){return d(e,{...t,method:`POST`})},DELETE(e,t){return d(e,{...t,method:`DELETE`})},OPTIONS(e,t){return d(e,{...t,method:`OPTIONS`})},HEAD(e,t){return d(e,{...t,method:`HEAD`})},PATCH(e,t){return d(e,{...t,method:`PATCH`})},TRACE(e,t){return d(e,{...t,method:`TRACE`})},use(...e){for(let t of e)if(t){if(typeof t!=`object`||!(`onRequest`in t||`onResponse`in t||`onError`in t))throw Error("Middleware must be an object with one of `onRequest()`, `onResponse() or `onError()`");u.push(t)}},eject(...e){for(let t of e){let e=u.indexOf(t);e!==-1&&u.splice(e,1)}}}}function V(e,t,n){if(t==null)return``;if(typeof t==`object`)throw Error("Deeply-nested arrays/objects aren’t supported. Provide your own `querySerializer()` to handle these.");return`${e}=${n?.allowReserved===!0?t:encodeURIComponent(t)}`}function at(e,t,n){if(!t||typeof t!=`object`)return``;let r=[],i={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`;if(n.style!==`deepObject`&&n.explode===!1){for(let e in t)r.push(e,n.allowReserved===!0?t[e]:encodeURIComponent(t[e]));let i=r.join(`,`);switch(n.style){case`form`:return`${e}=${i}`;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return i}}for(let i in t){let a=n.style===`deepObject`?`${e}[${i}]`:i;r.push(V(a,t[i],n))}let a=r.join(i);return n.style===`label`||n.style===`matrix`?`${i}${a}`:a}function ot(e,t,n){if(!Array.isArray(t))return``;if(n.explode===!1){let r={form:`,`,spaceDelimited:`%20`,pipeDelimited:`|`}[n.style]||`,`,i=(n.allowReserved===!0?t:t.map(e=>encodeURIComponent(e))).join(r);switch(n.style){case`simple`:return i;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return`${e}=${i}`}}let r={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`,i=[];for(let r of t)n.style===`simple`||n.style===`label`?i.push(n.allowReserved===!0?r:encodeURIComponent(r)):i.push(V(e,r,n));return n.style===`label`||n.style===`matrix`?`${r}${i.join(r)}`:i.join(r)}function st(e){return function(t){let n=[];if(t&&typeof t==`object`)for(let r in t){let i=t[r];if(i!=null){if(Array.isArray(i)){if(i.length===0)continue;n.push(ot(r,i,{style:`form`,explode:!0,...e?.array,allowReserved:e?.allowReserved||!1}));continue}if(typeof i==`object`){n.push(at(r,i,{style:`deepObject`,explode:!0,...e?.object,allowReserved:e?.allowReserved||!1}));continue}n.push(V(r,i,e))}}return n.join(`&`)}}function ct(e,t){let n=e;for(let r of e.match(pt)??[]){let e=r.substring(1,r.length-1),i=!1,a=`simple`;if(e.endsWith(`*`)&&(i=!0,e=e.substring(0,e.length-1)),e.startsWith(`.`)?(a=`label`,e=e.substring(1)):e.startsWith(`;`)&&(a=`matrix`,e=e.substring(1)),!t||t[e]===void 0||t[e]===null)continue;let o=t[e];if(Array.isArray(o)){n=n.replace(r,ot(e,o,{style:a,explode:i}));continue}if(typeof o==`object`){n=n.replace(r,at(e,o,{style:a,explode:i}));continue}if(a===`matrix`){n=n.replace(r,`;${V(e,o)}`);continue}n=n.replace(r,a===`label`?`.${encodeURIComponent(o)}`:encodeURIComponent(o))}return n}function lt(e,t){return e instanceof FormData?e:t&&(t.get instanceof Function?t.get(`Content-Type`)??t.get(`content-type`):t[`Content-Type`]??t[`content-type`])===`application/x-www-form-urlencoded`?new URLSearchParams(e).toString():JSON.stringify(e)}function ut(e,t){let n=`${t.baseUrl}${e}`;t.params?.path&&(n=t.pathSerializer(n,t.params.path));let r=t.querySerializer(t.params.query??{});return r.startsWith(`?`)&&(r=r.substring(1)),r&&(n+=`?${r}`),n}function dt(...e){let t=new Headers;for(let n of e){if(!n||typeof n!=`object`)continue;let e=n instanceof Headers?n.entries():Object.entries(n);for(let[n,r]of e)if(r===null)t.delete(n);else if(Array.isArray(r))for(let e of r)t.append(n,e);else r!==void 0&&t.set(n,r)}return t}function ft(e){return e.endsWith(`/`)?e.substring(0,e.length-1):e}var pt,mt;function ht(){return(ht=e((()=>{pt=/\{[^{}]+\}/g,mt=()=>typeof process==`object`&&Number.parseInt(process?.versions?.node?.substring(0,2))>=18&&process.versions.undici})))()}function gt(e){if(!e||typeof e!=`object`||Array.isArray(e))return{};let t=e,n=t.status===`error`&&t.details&&typeof t.details==`object`&&!Array.isArray(t.details)?t.details:t,r={};for(let[e,i]of Object.entries(n))if(!(n===t&&yt.has(e))){if(Array.isArray(i)){let t=i.filter(e=>typeof e==`string`);t.length>0&&(r[e]=t)}else typeof i==`string`&&(r[e]=[i])}return r}var H,_t,vt,yt;function bt(){return(bt=e((()=>{H=class extends Error{status;statusText;data;constructor(e,t,n){super(`HTTP ${e}: ${t}`),this.status=e,this.statusText=t,this.data=n,this.name=`HttpError`}},_t=class extends Error{cause;constructor(e){super(`Network request failed`),this.cause=e,this.name=`NetworkError`}},vt=class extends H{fieldErrors;constructor(e,t,n,r){super(e,t,n),this.fieldErrors=r,this.name=`ValidationError`}},yt=new Set([`detail`,`status`,`message`,`type`])})))()}function xt(){let e=document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);return e?decodeURIComponent(e[1]):``}function St(){let e=encodeURIComponent(window.location.pathname+window.location.search);throw window.location.href=`/utilisateur/connexion?next=${e}`,Error(`Redirecting to login`)}function Ct(e){let t=[`GET`,`POST`,`PUT`,`PATCH`,`DELETE`,`HEAD`,`OPTIONS`,`TRACE`],n={...e};for(let r of t){let t=e[r];n[r]=async(...e)=>{try{return await t(...e)}catch(e){throw e instanceof DOMException&&e.name===`AbortError`||e instanceof H||e instanceof Error&&e.message===`Redirecting to login`?e:new _t(e)}}}return n}var wt,Tt,U;function Et(){return(Et=e((()=>{ht(),bt(),wt={async onRequest({request:e}){if(e.method!==`GET`)return e.headers.set(`X-CSRFToken`,xt()),e}},Tt={async onResponse({response:e}){if(e.ok)return;e.status===401&&St();let t=await e.clone().json().catch(()=>void 0);throw e.status===400||e.status===422?new vt(e.status,e.statusText,t,gt(t)):new H(e.status,e.statusText,t)}},U=it({baseUrl:typeof window<`u`?window.location.origin:``,credentials:`same-origin`,fetch:(...e)=>globalThis.fetch(...e)}),U.use(wt),U.use(Tt),Ct(U)})))()}function Dt(){let e=document.createElement(`form`);e.method=`POST`,e.action=`/utilisateur/deconnexion`,e.hidden=!0;let t=document.createElement(`input`);t.type=`hidden`,t.name=`csrfmiddlewaretoken`,t.value=xt(),e.append(t),document.body.append(e),e.submit()}function Ot(){return(Ot=e((()=>{Et()})))()}function kt(){return typeof window>`u`?!1:window.matchMedia(`(prefers-color-scheme: dark)`).matches}function W(e){typeof document>`u`||document.documentElement.setAttribute(`data-fr-theme`,e?`dark`:`light`)}function At(){let e=_(()=>K.value===`system`?q.value:K.value===`dark`);function r(t){K.value=t,localStorage.setItem(G,t),W(e.value)}function i(){r(e.value?`light`:`dark`)}let a=null,o=null;return C(()=>{q.value=kt();let t=localStorage.getItem(G);t&&[`light`,`dark`,`system`].includes(t)&&(K.value=t),W(e.value),a=window.matchMedia(`(prefers-color-scheme: dark)`),o=e=>{q.value=e.matches,K.value===`system`&&W(e.matches)},a.addEventListener(`change`,o)}),n(()=>{a&&o&&a.removeEventListener(`change`,o)}),t(e,e=>{W(e)}),{colorMode:K,isDark:e,setColorMode:r,toggle:i}}var G,K,q;function jt(){return(jt=e((()=>{v(),G=`csp_color_mode`,K=y(`system`),q=y(!1)})))()}var Mt,Nt,Pt,Ft;function It(){return(It=e((()=>{v(),Ot(),ne(),j(),w(),jt(),R(),Mt={key:0,class:`csp-sidebar-user__info`,"data-testid":`sidebar-user-info`},Nt={class:`csp-sidebar-user__name`},Pt={key:0,class:`csp-sidebar-user__role`},Ft=l({__name:`CspSidebarUser`,props:{name:{},role:{}},setup(e){let{isExpanded:t,isMobile:n}=P(),{isDark:a,toggle:o}=At();return(c,l)=>(s(),f(M,{side:`right`,align:`end`,sections:[{items:[{label:p(a)?`Mode clair`:`Mode sombre`,icon:p(a)?`ri:sun-line`:`ri:moon-line`,onSelect:p(o)}]},{items:[{label:`Mon profil`,icon:`ri:user-line`},{label:`Paramètres`,icon:`ri:settings-3-line`}]},{items:[{label:`Se déconnecter`,icon:`ri:logout-box-r-line`,destructive:!0,onSelect:p(Dt)}]}]},{trigger:b(()=>[S(`button`,{type:`button`,class:m([`csp-sidebar-user`,{"csp-sidebar-user--expanded":p(t)||p(n)}])},[i(O,{name:e.name,size:`md`},null,8,[`name`]),p(t)||p(n)?(s(),x(`div`,Mt,[S(`span`,Nt,u(e.name),1),e.role?(s(),x(`span`,Pt,u(e.role),1)):r(``,!0)])):r(``,!0),p(t)||p(n)?(s(),f(T,{key:1,name:`ri:expand-up-down-line`,size:16,class:`csp-sidebar-user__chevron`})):r(``,!0)],2)]),_:1},8,[`sections`]))}})})))()}var Lt;function Rt(){return(Rt=e((()=>{It(),E(),Lt=D(Ft,[[`__scopeId`,`data-v-4d3828b4`]])})))()}var zt,J,Y,X,Z,Q,$,Bt;function Vt(){return(Vt=e((()=>{g(),Ne(),Re(),Ue(),Ye(),Qe(),nt(),Rt(),zt={title:`Compositions/Génériques/CspSidebar`,component:B,parameters:{layout:`fullscreen`,docs:{description:{component:'\nSidebar de navigation adaptée au DSFR.\n\n## Composants\n\n- `CspSidebarProvider` : contexte partagé (état, mobile, raccourcis)\n- `CspSidebar` : panneau de navigation\n- `CspSidebarTrigger` : bouton hamburger mobile (dans le header)\n- `CspSidebarGroup`, `CspSidebarItem`, `CspSidebarLogo`, `CspSidebarUser`\n\n## Usage\n\n```vue\n<CspAppShell :navigation="navigation">\n  <!-- contenu de page -->\n</CspAppShell>\n```\n        '}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},J=`
  <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
    <div style="display: flex; min-height: 100vh;">
      <aside style="flex-shrink: 0; border-right: 1px solid var(--border-default-grey);">
        <CspSidebar>
          <template #logo>
            <CspSidebarLogo />
          </template>

          <CspSidebarGroup>
            <CspSidebarItem icon="ri:dashboard-line" label="Première entrée" :to="{ path: '/premiere' }" />
            <CspSidebarItem icon="ri:briefcase-line" label="Entrée active" :to="{ path: '/active' }" :is-active="true" />
          </CspSidebarGroup>

          <CspSidebarGroup>
            <CspSidebarItem icon="ri:group-line" label="Troisième entrée" :to="{ path: '/troisieme' }" />
            <CspSidebarItem icon="ri:layout-column-line" label="Quatrième entrée" :to="{ path: '/quatrieme' }" />
          </CspSidebarGroup>

          <CspSidebarGroup>
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
`,Y={CspSidebar:Me,CspSidebarGroup:Le,CspSidebarItem:He,CspSidebarLogo:Je,CspSidebarProvider:B,CspSidebarTrigger:tt,CspSidebarUser:Lt},X={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Z={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Q={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},$={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:Y,setup(){let t=te();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
      <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
        <div style="display: flex; min-height: 100vh;">
          <aside style="flex-shrink: 0; border-right: 1px solid var(--border-default-grey);">
            <CspSidebar>
              <template #logo>
                <CspSidebarLogo />
              </template>

              <CspSidebarGroup>
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

              <CspSidebarGroup>
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
}`,...$.parameters?.docs?.source}}},Bt=[`Default`,`Collapsed`,`Mobile`,`WithRouterLinks`]})))()}Vt();export{Z as Collapsed,X as Default,Q as Mobile,$ as WithRouterLinks,Bt as __namedExportsOrder,zt as default};