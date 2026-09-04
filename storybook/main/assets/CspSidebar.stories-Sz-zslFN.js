import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,B as n,C as r,D as i,Dt as a,G as o,H as s,N as c,O as l,Ot as u,Q as d,S as f,St as p,Tt as m,U as h,a as g,b as _,c as v,ht as y,i as ee,rt as b,s as te,w as x,x as S,z as C}from"./iframe-CnJ3gxPo.js";import{n as w,t as T}from"./CspIcon-DEDutsQE.js";import{n as E,t as D}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as ne,t as O}from"./CspAvatar-DbXaH668.js";import{n as k,t as A}from"./Primitive-CyUMQID6.js";import{n as j,t as M}from"./CspDropdownMenu-bnYXAIt3.js";import{n as N,t as re}from"./CspTooltip-G7eGylld.js";import{a as ie,c as ae,i as oe,n as se,o as ce,r as le,s as ue,t as de}from"./DialogPortal-Cg43z3xN.js";import{n as fe,t as pe}from"./CspButton-DoWa-g7C.js";function me(e){let t=y(!1);function r(){typeof window<`u`&&(t.value=window.innerWidth<=e)}return C(()=>{r(),window.addEventListener(`resize`,r)}),n(()=>{window.removeEventListener(`resize`,r)}),t}function he(e){let{defaultExpanded:r=!0,persistState:i=!0}=e,a=localStorage.getItem(F),o=y(a===null?r:a===`true`),s=me(768),c=y(!1),l=_(()=>o.value?`expanded`:`collapsed`);function u(e){o.value=e,i&&localStorage.setItem(F,String(e))}function d(e){c.value=e}function f(){s.value?d(!c.value):u(!o.value)}function p(e){e.key===`b`&&(e.metaKey||e.ctrlKey)&&(e.preventDefault(),f())}C(()=>{window.addEventListener(`keydown`,p)}),n(()=>{window.removeEventListener(`keydown`,p)}),t(s,e=>{!e&&c.value&&(c.value=!1)});let m={state:l,isExpanded:o,isMobile:s,isMobileOpen:c,setExpanded:u,setMobileOpen:d,toggle:f};return h(L,m),m}function P(){let e=c(L);if(!e)throw Error(`useSidebar must be used within a CspSidebar provider`);return e}var F,I,ge,L;function R(){return(R=e((()=>{v(),F=`csp_sidebar_state`,I=`15rem`,ge=`4rem`,L=Symbol(`sidebar`)})))()}var _e,ve,ye,be,xe,Se,Ce,we,Te,Ee,De;function Oe(){return(Oe=e((()=>{v(),ce(),oe(),se(),ae(),fe(),w(),R(),_e={class:`csp-sidebar__header`},ve={key:0,class:`csp-sidebar__brand`},ye={class:`csp-sidebar__nav`},be={key:0,class:`csp-sidebar__footer`},xe=[`data-state`,`aria-expanded`],Se={class:`csp-sidebar__header`},Ce={key:0,class:`csp-sidebar__brand`},we=[`aria-label`,`title`],Te={class:`csp-sidebar__nav`},Ee={key:0,class:`csp-sidebar__footer`},De=l({__name:`CspSidebar`,setup(e){let t=d(),n=_(()=>!!t.logo),c=_(()=>!!t.footer),{state:l,isExpanded:u,isMobile:h,isMobileOpen:g,setMobileOpen:v,toggle:y}=P();return(e,t)=>p(h)?(s(),f(p(ue),{key:0,open:p(g),"onUpdate:open":p(v)},{default:b(()=>[i(p(de),null,{default:b(()=>[i(p(le),{class:`csp-sidebar-overlay`}),i(p(ie),{class:`csp-sidebar csp-sidebar--mobile`,"aria-label":e.$attrs[`aria-label`]??`Menu de navigation`,style:a({"--sidebar-width":p(I)})},{default:b(()=>[S(`header`,_e,[n.value?(s(),x(`div`,ve,[o(e.$slots,`logo`,{},void 0,!0)])):r(``,!0),i(pe,{class:`csp-sidebar__close`,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":`Fermer le menu`,onClick:t[0]||=e=>p(v)(!1)})]),S(`nav`,ye,[o(e.$slots,`default`,{},void 0,!0)]),c.value?(s(),x(`div`,be,[o(e.$slots,`footer`,{},void 0,!0)])):r(``,!0)]),_:3},8,[`aria-label`,`style`])]),_:3})]),_:3},8,[`open`,`onUpdate:open`])):(s(),x(`nav`,{key:1,class:m([`csp-sidebar`,{"csp-sidebar--expanded":p(u)}]),"data-state":p(l),"aria-expanded":p(u),style:a({"--sidebar-width":p(I),"--sidebar-width-collapsed":p(ge)})},[S(`div`,Se,[n.value&&p(u)?(s(),x(`div`,Ce,[o(e.$slots,`logo`,{},void 0,!0)])):r(``,!0),S(`button`,{type:`button`,class:`csp-sidebar__toggle`,"aria-label":p(u)?`Réduire le menu`:`Ouvrir le menu`,title:`${p(u)?`Réduire`:`Ouvrir`} (Ctrl+B)`,onClick:t[1]||=(...e)=>p(y)&&p(y)(...e)},[i(T,{name:p(u)?`ri:sidebar-fold-line`:`ri:sidebar-unfold-line`,size:18},null,8,[`name`])],8,we)]),S(`div`,Te,[o(e.$slots,`default`,{},void 0,!0)]),c.value?(s(),x(`div`,Ee,[o(e.$slots,`footer`,{},void 0,!0)])):r(``,!0)],14,xe))}})})))()}var ke;function Ae(){return(Ae=e((()=>{Oe(),E(),ke=D(De,[[`__scopeId`,`data-v-40fc1d50`]])})))()}function je(e,t){return s(),x(`div`,Me,[S(`div`,Ne,[o(e.$slots,`default`,{},void 0,!0)])])}var z,Me,Ne,Pe;function Fe(){return(Fe=e((()=>{v(),E(),z={},Me={class:`csp-sidebar-group`},Ne={class:`csp-sidebar-group__items`},Pe=D(z,[[`render`,je],[`__scopeId`,`data-v-a36d535a`]]),z.__docgenInfo=Object.assign({displayName:z.name??z.__name},{exportName:`default`,displayName:`CspSidebarGroup`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey`,schema:`PropertyKey`,declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef`,schema:`VNodeRef`,declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean`,schema:`boolean`,declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string`,schema:`string`,declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[]`,schema:`VNodeUpdateHook | VNodeUpdateHook[]`,declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[]`,schema:`VNodeUpdateHook | VNodeUpdateHook[]`,declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[{name:`default`,type:`{}`,description:``,tags:[],schema:`{}`,declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarGroup.vue`})})))()}var Ie,Le;function Re(){return(Re=e((()=>{v(),k(),g(),w(),N(),R(),Ie={key:0,class:`csp-sidebar-item__label`},Le=l({inheritAttrs:!1,__name:`CspSidebarItem`,props:{icon:{},label:{},to:{},isActive:{type:Boolean,default:!1}},setup(e){let{isExpanded:t,isMobile:n}=P();return(a,o)=>(s(),f(re,{content:e.label,disabled:p(t)||p(n),side:`right`,"side-offset":12},{default:b(()=>[i(p(A),{as:e.to?p(ee):`button`,to:e.to,type:e.to?void 0:`button`,class:m([`csp-sidebar-item`,{"csp-sidebar-item--active":e.isActive,"csp-sidebar-item--expanded":p(t)||p(n)}]),"aria-current":e.isActive?`page`:void 0},{default:b(()=>[i(T,{class:`csp-sidebar-item__icon`,name:e.icon,size:16},null,8,[`name`]),p(t)||p(n)?(s(),x(`span`,Ie,u(e.label),1)):r(``,!0)]),_:1},8,[`as`,`to`,`type`,`class`,`aria-current`])]),_:1},8,[`content`,`disabled`]))}})})))()}var ze;function Be(){return(Be=e((()=>{Re(),E(),ze=D(Le,[[`__scopeId`,`data-v-d69b2512`]])})))()}var Ve,He,Ue;function We(){return(We=e((()=>{v(),R(),Ve={class:`csp-sidebar-logo`},He={key:0,class:`csp-sidebar-logo__subtitle`},Ue=l({__name:`CspSidebarLogo`,setup(e){let{isExpanded:t,isMobile:n}=P();return(e,i)=>(s(),x(`div`,Ve,[i[0]||=S(`span`,{class:`csp-sidebar-logo__title`},`CSPLab`,-1),p(t)||p(n)?(s(),x(`span`,He,` ATS `)):r(``,!0)]))}})})))()}var Ge;function Ke(){return(Ke=e((()=>{We(),E(),Ge=D(Ue,[[`__scopeId`,`data-v-8492f1ff`]])})))()}var qe;function Je(){return(Je=e((()=>{v(),R(),qe=l({__name:`CspSidebarProvider`,props:{defaultExpanded:{type:Boolean,default:!0},persistState:{type:Boolean,default:!0}},setup(e){let t=e;return he({defaultExpanded:t.defaultExpanded,persistState:t.persistState}),(e,t)=>o(e.$slots,`default`)}})})))()}var B;function Ye(){return(Ye=e((()=>{Je(),B=qe})))()}var Xe;function Ze(){return(Ze=e((()=>{v(),fe(),R(),Xe=l({__name:`CspSidebarTrigger`,setup(e){let{toggle:t,isMobile:n}=P();return(e,i)=>p(n)?(s(),f(pe,{key:0,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:menu-line`,"aria-label":`Ouvrir le menu`,onClick:p(t)},null,8,[`onClick`])):r(``,!0)}})})))()}var Qe;function $e(){return($e=e((()=>{Ze(),Qe=Xe})))()}function et(){return Math.random().toString(36).slice(2,11)}function tt(e){let{baseUrl:t=``,Request:n=globalThis.Request,fetch:r=globalThis.fetch,querySerializer:i,bodySerializer:a,pathSerializer:o,headers:s,requestInitExt:c=void 0,...l}={...e};c=dt()?c:void 0,t=lt(t);let u=[];async function d(e,d){let{baseUrl:f,fetch:p=r,Request:m=n,headers:h,params:g={},parseAs:_=`json`,querySerializer:v,bodySerializer:y=a??ot,pathSerializer:ee,body:b,middleware:te=[],...x}=d||{},S=t;f&&(S=lt(f)??t);let C=typeof i==`function`?i:it(i);v&&(C=typeof v==`function`?v:it({...typeof i==`object`?i:{},...v}));let w=ee||o||at,T=b===void 0?void 0:y(b,ct(s,h,g.header)),E=ct(T===void 0||T instanceof FormData?{}:{"Content-Type":`application/json`},s,h,g.header),D=[...u,...te],ne={redirect:`follow`,...l,...x,body:T,headers:E},O,k,A=new m(st(e,{baseUrl:S,params:g,querySerializer:C,pathSerializer:w}),ne),j;for(let e in x)e in A||(A[e]=x[e]);if(D.length){O=et(),k=Object.freeze({baseUrl:S,fetch:p,parseAs:_,querySerializer:C,bodySerializer:y,pathSerializer:w});for(let t of D)if(t&&typeof t==`object`&&typeof t.onRequest==`function`){let n=await t.onRequest({request:A,schemaPath:e,params:g,options:k,id:O});if(n){if(n instanceof m)A=n;else if(n instanceof Response){j=n;break}else throw Error(`onRequest: must return new Request() or Response() when modifying the request`)}}}if(!j){try{j=await p(A,c)}catch(t){let n=t;if(D.length)for(let t=D.length-1;t>=0;t--){let r=D[t];if(r&&typeof r==`object`&&typeof r.onError==`function`){let t=await r.onError({request:A,error:n,schemaPath:e,params:g,options:k,id:O});if(t){if(t instanceof Response){n=void 0,j=t;break}if(t instanceof Error){n=t;continue}throw Error(`onError: must return new Response() or instance of Error`)}}}if(n)throw n}if(D.length)for(let t=D.length-1;t>=0;t--){let n=D[t];if(n&&typeof n==`object`&&typeof n.onResponse==`function`){let t=await n.onResponse({request:A,response:j,schemaPath:e,params:g,options:k,id:O});if(t){if(!(t instanceof Response))throw Error(`onResponse: must return new Response() when modifying the response`);j=t}}}}let M=j.headers.get(`Content-Length`);if(j.status===204||A.method===`HEAD`||M===`0`&&!j.headers.get(`Transfer-Encoding`)?.includes(`chunked`))return j.ok?{data:void 0,response:j}:{error:void 0,response:j};if(j.ok)return{data:await(async()=>{if(_===`stream`)return j.body;if(_===`json`&&!M){let e=await j.text();return e?JSON.parse(e):void 0}return await j[_]()})(),response:j};let N=await j.text();try{N=JSON.parse(N)}catch{}return{error:N,response:j}}return{request(e,t,n){return d(t,{...n,method:e.toUpperCase()})},GET(e,t){return d(e,{...t,method:`GET`})},PUT(e,t){return d(e,{...t,method:`PUT`})},POST(e,t){return d(e,{...t,method:`POST`})},DELETE(e,t){return d(e,{...t,method:`DELETE`})},OPTIONS(e,t){return d(e,{...t,method:`OPTIONS`})},HEAD(e,t){return d(e,{...t,method:`HEAD`})},PATCH(e,t){return d(e,{...t,method:`PATCH`})},TRACE(e,t){return d(e,{...t,method:`TRACE`})},use(...e){for(let t of e)if(t){if(typeof t!=`object`||!(`onRequest`in t||`onResponse`in t||`onError`in t))throw Error("Middleware must be an object with one of `onRequest()`, `onResponse() or `onError()`");u.push(t)}},eject(...e){for(let t of e){let e=u.indexOf(t);e!==-1&&u.splice(e,1)}}}}function V(e,t,n){if(t==null)return``;if(typeof t==`object`)throw Error("Deeply-nested arrays/objects aren’t supported. Provide your own `querySerializer()` to handle these.");return`${e}=${n?.allowReserved===!0?t:encodeURIComponent(t)}`}function nt(e,t,n){if(!t||typeof t!=`object`)return``;let r=[],i={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`;if(n.style!==`deepObject`&&n.explode===!1){for(let e in t)r.push(e,n.allowReserved===!0?t[e]:encodeURIComponent(t[e]));let i=r.join(`,`);switch(n.style){case`form`:return`${e}=${i}`;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return i}}for(let i in t){let a=n.style===`deepObject`?`${e}[${i}]`:i;r.push(V(a,t[i],n))}let a=r.join(i);return n.style===`label`||n.style===`matrix`?`${i}${a}`:a}function rt(e,t,n){if(!Array.isArray(t))return``;if(n.explode===!1){let r={form:`,`,spaceDelimited:`%20`,pipeDelimited:`|`}[n.style]||`,`,i=(n.allowReserved===!0?t:t.map(e=>encodeURIComponent(e))).join(r);switch(n.style){case`simple`:return i;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return`${e}=${i}`}}let r={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`,i=[];for(let r of t)n.style===`simple`||n.style===`label`?i.push(n.allowReserved===!0?r:encodeURIComponent(r)):i.push(V(e,r,n));return n.style===`label`||n.style===`matrix`?`${r}${i.join(r)}`:i.join(r)}function it(e){return function(t){let n=[];if(t&&typeof t==`object`)for(let r in t){let i=t[r];if(i!=null){if(Array.isArray(i)){if(i.length===0)continue;n.push(rt(r,i,{style:`form`,explode:!0,...e?.array,allowReserved:e?.allowReserved||!1}));continue}if(typeof i==`object`){n.push(nt(r,i,{style:`deepObject`,explode:!0,...e?.object,allowReserved:e?.allowReserved||!1}));continue}n.push(V(r,i,e))}}return n.join(`&`)}}function at(e,t){let n=e;for(let r of e.match(ut)??[]){let e=r.substring(1,r.length-1),i=!1,a=`simple`;if(e.endsWith(`*`)&&(i=!0,e=e.substring(0,e.length-1)),e.startsWith(`.`)?(a=`label`,e=e.substring(1)):e.startsWith(`;`)&&(a=`matrix`,e=e.substring(1)),!t||t[e]===void 0||t[e]===null)continue;let o=t[e];if(Array.isArray(o)){n=n.replace(r,rt(e,o,{style:a,explode:i}));continue}if(typeof o==`object`){n=n.replace(r,nt(e,o,{style:a,explode:i}));continue}if(a===`matrix`){n=n.replace(r,`;${V(e,o)}`);continue}n=n.replace(r,a===`label`?`.${encodeURIComponent(o)}`:encodeURIComponent(o))}return n}function ot(e,t){return e instanceof FormData?e:t&&(t.get instanceof Function?t.get(`Content-Type`)??t.get(`content-type`):t[`Content-Type`]??t[`content-type`])===`application/x-www-form-urlencoded`?new URLSearchParams(e).toString():JSON.stringify(e)}function st(e,t){let n=`${t.baseUrl}${e}`;t.params?.path&&(n=t.pathSerializer(n,t.params.path));let r=t.querySerializer(t.params.query??{});return r.startsWith(`?`)&&(r=r.substring(1)),r&&(n+=`?${r}`),n}function ct(...e){let t=new Headers;for(let n of e){if(!n||typeof n!=`object`)continue;let e=n instanceof Headers?n.entries():Object.entries(n);for(let[n,r]of e)if(r===null)t.delete(n);else if(Array.isArray(r))for(let e of r)t.append(n,e);else r!==void 0&&t.set(n,r)}return t}function lt(e){return e.endsWith(`/`)?e.substring(0,e.length-1):e}var ut,dt;function ft(){return(ft=e((()=>{ut=/\{[^{}]+\}/g,dt=()=>typeof process==`object`&&Number.parseInt(process?.versions?.node?.substring(0,2))>=18&&process.versions.undici})))()}function pt(e){if(!e||typeof e!=`object`||Array.isArray(e))return{};let t=e,n=t.status===`error`&&t.details&&typeof t.details==`object`&&!Array.isArray(t.details)?t.details:t,r={};for(let[e,i]of Object.entries(n))if(!(n===t&&gt.has(e))){if(Array.isArray(i)){let t=i.filter(e=>typeof e==`string`);t.length>0&&(r[e]=t)}else typeof i==`string`&&(r[e]=[i])}return r}var H,mt,ht,gt;function _t(){return(_t=e((()=>{H=class extends Error{status;statusText;data;constructor(e,t,n){super(`HTTP ${e}: ${t}`),this.status=e,this.statusText=t,this.data=n,this.name=`HttpError`}},mt=class extends Error{cause;constructor(e){super(`Network request failed`),this.cause=e,this.name=`NetworkError`}},ht=class extends H{fieldErrors;constructor(e,t,n,r){super(e,t,n),this.fieldErrors=r,this.name=`ValidationError`}},gt=new Set([`detail`,`status`,`message`,`type`])})))()}function vt(){let e=document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);return e?decodeURIComponent(e[1]):``}function yt(){let e=encodeURIComponent(window.location.pathname+window.location.search);throw window.location.href=`/utilisateur/connexion?next=${e}`,Error(`Redirecting to login`)}function bt(e){let t=[`GET`,`POST`,`PUT`,`PATCH`,`DELETE`,`HEAD`,`OPTIONS`,`TRACE`],n={...e};for(let r of t){let t=e[r];n[r]=async(...e)=>{try{return await t(...e)}catch(e){throw e instanceof DOMException&&e.name===`AbortError`||e instanceof H||e instanceof Error&&e.message===`Redirecting to login`?e:new mt(e)}}}return n}var xt,St,U;function Ct(){return(Ct=e((()=>{ft(),_t(),xt={async onRequest({request:e}){if(e.method!==`GET`)return e.headers.set(`X-CSRFToken`,vt()),e}},St={async onResponse({response:e}){if(e.ok)return;e.status===401&&yt();let t=await e.clone().json().catch(()=>void 0);throw e.status===400||e.status===422?new ht(e.status,e.statusText,t,pt(t)):new H(e.status,e.statusText,t)}},U=tt({baseUrl:typeof window<`u`?window.location.origin:``,credentials:`same-origin`,fetch:(...e)=>globalThis.fetch(...e)}),U.use(xt),U.use(St),bt(U)})))()}function wt(){let e=document.createElement(`form`);e.method=`POST`,e.action=`/utilisateur/deconnexion`,e.hidden=!0;let t=document.createElement(`input`);t.type=`hidden`,t.name=`csrfmiddlewaretoken`,t.value=vt(),e.append(t),document.body.append(e),e.submit()}function Tt(){return(Tt=e((()=>{Ct()})))()}function Et(){return typeof window>`u`?!1:window.matchMedia(`(prefers-color-scheme: dark)`).matches}function W(e){typeof document>`u`||document.documentElement.setAttribute(`data-fr-theme`,e?`dark`:`light`)}function Dt(){let e=_(()=>K.value===`system`?q.value:K.value===`dark`);function r(t){K.value=t,localStorage.setItem(G,t),W(e.value)}function i(){r(e.value?`light`:`dark`)}let a=null,o=null;return C(()=>{q.value=Et();let t=localStorage.getItem(G);t&&[`light`,`dark`,`system`].includes(t)&&(K.value=t),W(e.value),a=window.matchMedia(`(prefers-color-scheme: dark)`),o=e=>{q.value=e.matches,K.value===`system`&&W(e.matches)},a.addEventListener(`change`,o)}),n(()=>{a&&o&&a.removeEventListener(`change`,o)}),t(e,e=>{W(e)}),{colorMode:K,isDark:e,setColorMode:r,toggle:i}}var G,K,q;function Ot(){return(Ot=e((()=>{v(),G=`csp_color_mode`,K=y(`system`),q=y(!1)})))()}var kt,At,jt,Mt;function Nt(){return(Nt=e((()=>{v(),Tt(),ne(),j(),w(),Ot(),R(),kt={key:0,class:`csp-sidebar-user__info`,"data-testid":`sidebar-user-info`},At={class:`csp-sidebar-user__name`},jt={key:0,class:`csp-sidebar-user__role`},Mt=l({__name:`CspSidebarUser`,props:{name:{},role:{}},setup(e){let{isExpanded:t,isMobile:n}=P(),{isDark:a,toggle:o}=Dt();return(c,l)=>(s(),f(M,{side:`right`,align:`end`,sections:[{items:[{label:p(a)?`Mode clair`:`Mode sombre`,icon:p(a)?`ri:sun-line`:`ri:moon-line`,onSelect:p(o)}]},{items:[{label:`Mon profil`,icon:`ri:user-line`},{label:`Paramètres`,icon:`ri:settings-3-line`}]},{items:[{label:`Se déconnecter`,icon:`ri:logout-box-r-line`,destructive:!0,onSelect:p(wt)}]}]},{trigger:b(()=>[S(`button`,{type:`button`,class:m([`csp-sidebar-user`,{"csp-sidebar-user--expanded":p(t)||p(n)}])},[i(O,{name:e.name,size:`md`},null,8,[`name`]),p(t)||p(n)?(s(),x(`div`,kt,[S(`span`,At,u(e.name),1),e.role?(s(),x(`span`,jt,u(e.role),1)):r(``,!0)])):r(``,!0),p(t)||p(n)?(s(),f(T,{key:1,name:`ri:expand-up-down-line`,size:16,class:`csp-sidebar-user__chevron`})):r(``,!0)],2)]),_:1},8,[`sections`]))}})})))()}var Pt;function Ft(){return(Ft=e((()=>{Nt(),E(),Pt=D(Mt,[[`__scopeId`,`data-v-4d3828b4`]])})))()}var It,J,Y,X,Z,Q,$,Lt;function Rt(){return(Rt=e((()=>{g(),Ae(),Fe(),Be(),Ke(),Ye(),$e(),Ft(),It={title:`Compositions/Génériques/CspSidebar`,component:B,parameters:{layout:`fullscreen`,docs:{description:{component:'\nSidebar de navigation adaptée au DSFR.\n\n## Composants\n\n- `CspSidebarProvider` : contexte partagé (état, mobile, raccourcis)\n- `CspSidebar` : panneau de navigation\n- `CspSidebarTrigger` : bouton hamburger mobile (dans le header)\n- `CspSidebarGroup`, `CspSidebarItem`, `CspSidebarLogo`, `CspSidebarUser`\n\n## Usage\n\n```vue\n<CspAppShell :navigation="navigation">\n  <!-- contenu de page -->\n</CspAppShell>\n```\n        '}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},J=`
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
`,Y={CspSidebar:ke,CspSidebarGroup:Pe,CspSidebarItem:ze,CspSidebarLogo:Ge,CspSidebarProvider:B,CspSidebarTrigger:Qe,CspSidebarUser:Pt},X={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Z={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Q={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},$={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:Y,setup(){let t=te();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
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
}`,...$.parameters?.docs?.source}}},Lt=[`Default`,`Collapsed`,`Mobile`,`WithRouterLinks`]})))()}Rt();export{Z as Collapsed,X as Default,Q as Mobile,$ as WithRouterLinks,Lt as __namedExportsOrder,It as default};