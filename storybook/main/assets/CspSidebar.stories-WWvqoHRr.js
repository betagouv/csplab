import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,Dt as r,E as i,Et as a,H as o,M as s,Q as c,R as l,S as u,V as d,W as f,Z as p,a as m,b as h,c as g,i as _,mt as v,nt as y,s as ee,wt as b,x,xt as S,y as C,z as w}from"./iframe-0WG_GZvT.js";import{n as T,t as E}from"./CspIcon-BEJFNvN2.js";import{n as D,t as O}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as te,t as k}from"./CspAvatar-BU71nlMh.js";import{n as A,t as j}from"./Primitive-SThVzp_0.js";import{n as M,t as ne}from"./CspDropdownMenu-D2T4NsuK.js";import{n as N,t as re}from"./CspTooltip-BK_Dkegl.js";import{a as ie,c as ae,i as oe,n as se,o as ce,r as le,s as ue,t as de}from"./DialogPortal-HSZ8Rtfl.js";import{n as fe,t as pe}from"./CspButton-6xtREjLY.js";function me(e){let t=v(!1);function n(){typeof window<`u`&&(t.value=window.innerWidth<=e)}return l(()=>{n(),window.addEventListener(`resize`,n)}),w(()=>{window.removeEventListener(`resize`,n)}),t}function he(e){let{defaultExpanded:t=!0,persistState:n=!0}=e,r=localStorage.getItem(F),i=v(r===null?t:r===`true`),a=me(768),s=v(!1),u=C(()=>i.value?`expanded`:`collapsed`);function d(e){i.value=e,n&&localStorage.setItem(F,String(e))}function f(e){s.value=e}function p(){a.value?f(!s.value):d(!i.value)}function m(e){e.key===`b`&&(e.metaKey||e.ctrlKey)&&(e.preventDefault(),p())}l(()=>{window.addEventListener(`keydown`,m)}),w(()=>{window.removeEventListener(`keydown`,m)}),c(a,e=>{!e&&s.value&&(s.value=!1)});let h={state:u,isExpanded:i,isMobile:a,isMobileOpen:s,setExpanded:d,setMobileOpen:f,toggle:p};return o(L,h),h}function P(){let e=s(L);if(!e)throw Error(`useSidebar must be used within a CspSidebar provider`);return e}var F,I,ge,L;function R(){return(R=e((()=>{g(),F=`csp_sidebar_state`,I=`15rem`,ge=`4rem`,L=Symbol(`sidebar`)})))()}var _e,ve,ye,be,xe,Se,Ce,we,Te,Ee,De;function Oe(){return(Oe=e((()=>{g(),ce(),oe(),se(),ae(),fe(),T(),R(),_e={class:`csp-sidebar__header`},ve={key:0,class:`csp-sidebar__brand`},ye={class:`csp-sidebar__nav`},be={key:0,class:`csp-sidebar__footer`},xe=[`data-state`,`aria-expanded`],Se={class:`csp-sidebar__header`},Ce={key:0,class:`csp-sidebar__brand`},we=[`aria-label`,`title`],Te={class:`csp-sidebar__nav`},Ee={key:0,class:`csp-sidebar__footer`},De=n({__name:`CspSidebar`,setup(e){let n=p(),r=C(()=>!!n.logo),o=C(()=>!!n.footer),{state:s,isExpanded:c,isMobile:l,isMobileOpen:m,setMobileOpen:g,toggle:_}=P();return(e,n)=>S(l)?(d(),x(S(ue),{key:0,open:S(m),"onUpdate:open":S(g)},{default:y(()=>[i(S(de),null,{default:y(()=>[i(S(le),{class:`csp-sidebar-overlay`}),i(S(ie),{class:`csp-sidebar csp-sidebar--mobile`,"aria-label":e.$attrs[`aria-label`]??`Menu de navigation`,style:a({"--sidebar-width":S(I)})},{default:y(()=>[h(`header`,_e,[r.value?(d(),t(`div`,ve,[f(e.$slots,`logo`,{},void 0,!0)])):u(``,!0),i(pe,{class:`csp-sidebar__close`,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":`Fermer le menu`,onClick:n[0]||=e=>S(g)(!1)})]),h(`nav`,ye,[f(e.$slots,`default`,{},void 0,!0)]),o.value?(d(),t(`div`,be,[f(e.$slots,`footer`,{},void 0,!0)])):u(``,!0)]),_:3},8,[`aria-label`,`style`])]),_:3})]),_:3},8,[`open`,`onUpdate:open`])):(d(),t(`nav`,{key:1,class:b([`csp-sidebar`,{"csp-sidebar--expanded":S(c)}]),"data-state":S(s),"aria-expanded":S(c),style:a({"--sidebar-width":S(I),"--sidebar-width-collapsed":S(ge)})},[h(`div`,Se,[r.value&&S(c)?(d(),t(`div`,Ce,[f(e.$slots,`logo`,{},void 0,!0)])):u(``,!0),h(`button`,{type:`button`,class:`csp-sidebar__toggle`,"aria-label":S(c)?`Réduire le menu`:`Ouvrir le menu`,title:`${S(c)?`Réduire`:`Ouvrir`} (Ctrl+B)`,onClick:n[1]||=(...e)=>S(_)&&S(_)(...e)},[i(E,{name:S(c)?`ri:sidebar-fold-line`:`ri:sidebar-unfold-line`,size:18},null,8,[`name`])],8,we)]),h(`div`,Te,[f(e.$slots,`default`,{},void 0,!0)]),o.value?(d(),t(`div`,Ee,[f(e.$slots,`footer`,{},void 0,!0)])):u(``,!0)],14,xe))}})})))()}var ke;function Ae(){return(Ae=e((()=>{Oe(),D(),ke=O(De,[[`__scopeId`,`data-v-40fc1d50`]])})))()}function je(e,n){return d(),t(`div`,Me,[h(`div`,Ne,[f(e.$slots,`default`,{},void 0,!0)])])}var z,Me,Ne,Pe;function Fe(){return(Fe=e((()=>{g(),D(),z={},Me={class:`csp-sidebar-group`},Ne={class:`csp-sidebar-group__items`},Pe=O(z,[[`render`,je],[`__scopeId`,`data-v-a36d535a`]]),z.__docgenInfo=Object.assign({displayName:z.name??z.__name},{exportName:`default`,displayName:`CspSidebarGroup`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey`,schema:`PropertyKey`,declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef`,schema:`VNodeRef`,declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean`,schema:`boolean`,declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string`,schema:`string`,declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[]`,schema:`VNodeUpdateHook | VNodeUpdateHook[]`,declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[]`,schema:`VNodeUpdateHook | VNodeUpdateHook[]`,declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[{name:`default`,type:`{}`,description:``,tags:[],schema:`{}`,declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarGroup.vue`})})))()}var Ie,Le;function Re(){return(Re=e((()=>{g(),A(),m(),T(),N(),R(),Ie={key:0,class:`csp-sidebar-item__label`},Le=n({inheritAttrs:!1,__name:`CspSidebarItem`,props:{icon:{},label:{},to:{},isActive:{type:Boolean,default:!1}},setup(e){let{isExpanded:n,isMobile:a}=P();return(o,s)=>(d(),x(re,{content:e.label,disabled:S(n)||S(a),side:`right`,"side-offset":12},{default:y(()=>[i(S(j),{as:e.to?S(_):`button`,to:e.to,type:e.to?void 0:`button`,class:b([`csp-sidebar-item`,{"csp-sidebar-item--active":e.isActive,"csp-sidebar-item--expanded":S(n)||S(a)}]),"aria-current":e.isActive?`page`:void 0},{default:y(()=>[i(E,{class:`csp-sidebar-item__icon`,name:e.icon,size:16},null,8,[`name`]),S(n)||S(a)?(d(),t(`span`,Ie,r(e.label),1)):u(``,!0)]),_:1},8,[`as`,`to`,`type`,`class`,`aria-current`])]),_:1},8,[`content`,`disabled`]))}})})))()}var ze;function Be(){return(Be=e((()=>{Re(),D(),ze=O(Le,[[`__scopeId`,`data-v-d69b2512`]])})))()}var Ve,He,Ue;function We(){return(We=e((()=>{g(),R(),Ve={class:`csp-sidebar-logo`},He={key:0,class:`csp-sidebar-logo__subtitle`},Ue=n({__name:`CspSidebarLogo`,setup(e){let{isExpanded:n,isMobile:r}=P();return(e,i)=>(d(),t(`div`,Ve,[i[0]||=h(`span`,{class:`csp-sidebar-logo__title`},`CSPLab`,-1),S(n)||S(r)?(d(),t(`span`,He,` ATS `)):u(``,!0)]))}})})))()}var Ge;function Ke(){return(Ke=e((()=>{We(),D(),Ge=O(Ue,[[`__scopeId`,`data-v-8492f1ff`]])})))()}var qe;function Je(){return(Je=e((()=>{g(),R(),qe=n({__name:`CspSidebarProvider`,props:{defaultExpanded:{type:Boolean,default:!0},persistState:{type:Boolean,default:!0}},setup(e){let t=e;return he({defaultExpanded:t.defaultExpanded,persistState:t.persistState}),(e,t)=>f(e.$slots,`default`)}})})))()}var B;function Ye(){return(Ye=e((()=>{Je(),B=qe})))()}var Xe;function Ze(){return(Ze=e((()=>{g(),fe(),R(),Xe=n({__name:`CspSidebarTrigger`,setup(e){let{toggle:t,isMobile:n}=P();return(e,r)=>S(n)?(d(),x(pe,{key:0,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:menu-line`,"aria-label":`Ouvrir le menu`,onClick:S(t)},null,8,[`onClick`])):u(``,!0)}})})))()}var Qe;function $e(){return($e=e((()=>{Ze(),Qe=Xe})))()}function et(){return Math.random().toString(36).slice(2,11)}function tt(e){let{baseUrl:t=``,Request:n=globalThis.Request,fetch:r=globalThis.fetch,querySerializer:i,bodySerializer:a,pathSerializer:o,headers:s,requestInitExt:c=void 0,...l}={...e};c=dt()?c:void 0,t=lt(t);let u=[];async function d(e,d){let{baseUrl:f,fetch:p=r,Request:m=n,headers:h,params:g={},parseAs:_=`json`,querySerializer:v,bodySerializer:y=a??ot,pathSerializer:ee,body:b,middleware:x=[],...S}=d||{},C=t;f&&(C=lt(f)??t);let w=typeof i==`function`?i:it(i);v&&(w=typeof v==`function`?v:it({...typeof i==`object`?i:{},...v}));let T=ee||o||at,E=b===void 0?void 0:y(b,ct(s,h,g.header)),D=ct(E===void 0||E instanceof FormData?{}:{"Content-Type":`application/json`},s,h,g.header),O=[...u,...x],te={redirect:`follow`,...l,...S,body:E,headers:D},k,A,j=new m(st(e,{baseUrl:C,params:g,querySerializer:w,pathSerializer:T}),te),M;for(let e in S)e in j||(j[e]=S[e]);if(O.length){k=et(),A=Object.freeze({baseUrl:C,fetch:p,parseAs:_,querySerializer:w,bodySerializer:y,pathSerializer:T});for(let t of O)if(t&&typeof t==`object`&&typeof t.onRequest==`function`){let n=await t.onRequest({request:j,schemaPath:e,params:g,options:A,id:k});if(n){if(n instanceof m)j=n;else if(n instanceof Response){M=n;break}else throw Error(`onRequest: must return new Request() or Response() when modifying the request`)}}}if(!M){try{M=await p(j,c)}catch(t){let n=t;if(O.length)for(let t=O.length-1;t>=0;t--){let r=O[t];if(r&&typeof r==`object`&&typeof r.onError==`function`){let t=await r.onError({request:j,error:n,schemaPath:e,params:g,options:A,id:k});if(t){if(t instanceof Response){n=void 0,M=t;break}if(t instanceof Error){n=t;continue}throw Error(`onError: must return new Response() or instance of Error`)}}}if(n)throw n}if(O.length)for(let t=O.length-1;t>=0;t--){let n=O[t];if(n&&typeof n==`object`&&typeof n.onResponse==`function`){let t=await n.onResponse({request:j,response:M,schemaPath:e,params:g,options:A,id:k});if(t){if(!(t instanceof Response))throw Error(`onResponse: must return new Response() when modifying the response`);M=t}}}}let ne=M.headers.get(`Content-Length`);if(M.status===204||j.method===`HEAD`||ne===`0`&&!M.headers.get(`Transfer-Encoding`)?.includes(`chunked`))return M.ok?{data:void 0,response:M}:{error:void 0,response:M};if(M.ok)return{data:await(async()=>{if(_===`stream`)return M.body;if(_===`json`&&!ne){let e=await M.text();return e?JSON.parse(e):void 0}return await M[_]()})(),response:M};let N=await M.text();try{N=JSON.parse(N)}catch{}return{error:N,response:M}}return{request(e,t,n){return d(t,{...n,method:e.toUpperCase()})},GET(e,t){return d(e,{...t,method:`GET`})},PUT(e,t){return d(e,{...t,method:`PUT`})},POST(e,t){return d(e,{...t,method:`POST`})},DELETE(e,t){return d(e,{...t,method:`DELETE`})},OPTIONS(e,t){return d(e,{...t,method:`OPTIONS`})},HEAD(e,t){return d(e,{...t,method:`HEAD`})},PATCH(e,t){return d(e,{...t,method:`PATCH`})},TRACE(e,t){return d(e,{...t,method:`TRACE`})},use(...e){for(let t of e)if(t){if(typeof t!=`object`||!(`onRequest`in t||`onResponse`in t||`onError`in t))throw Error("Middleware must be an object with one of `onRequest()`, `onResponse() or `onError()`");u.push(t)}},eject(...e){for(let t of e){let e=u.indexOf(t);e!==-1&&u.splice(e,1)}}}}function V(e,t,n){if(t==null)return``;if(typeof t==`object`)throw Error("Deeply-nested arrays/objects aren’t supported. Provide your own `querySerializer()` to handle these.");return`${e}=${n?.allowReserved===!0?t:encodeURIComponent(t)}`}function nt(e,t,n){if(!t||typeof t!=`object`)return``;let r=[],i={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`;if(n.style!==`deepObject`&&n.explode===!1){for(let e in t)r.push(e,n.allowReserved===!0?t[e]:encodeURIComponent(t[e]));let i=r.join(`,`);switch(n.style){case`form`:return`${e}=${i}`;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return i}}for(let i in t){let a=n.style===`deepObject`?`${e}[${i}]`:i;r.push(V(a,t[i],n))}let a=r.join(i);return n.style===`label`||n.style===`matrix`?`${i}${a}`:a}function rt(e,t,n){if(!Array.isArray(t))return``;if(n.explode===!1){let r={form:`,`,spaceDelimited:`%20`,pipeDelimited:`|`}[n.style]||`,`,i=(n.allowReserved===!0?t:t.map(e=>encodeURIComponent(e))).join(r);switch(n.style){case`simple`:return i;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return`${e}=${i}`}}let r={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`,i=[];for(let r of t)n.style===`simple`||n.style===`label`?i.push(n.allowReserved===!0?r:encodeURIComponent(r)):i.push(V(e,r,n));return n.style===`label`||n.style===`matrix`?`${r}${i.join(r)}`:i.join(r)}function it(e){return function(t){let n=[];if(t&&typeof t==`object`)for(let r in t){let i=t[r];if(i!=null){if(Array.isArray(i)){if(i.length===0)continue;n.push(rt(r,i,{style:`form`,explode:!0,...e?.array,allowReserved:e?.allowReserved||!1}));continue}if(typeof i==`object`){n.push(nt(r,i,{style:`deepObject`,explode:!0,...e?.object,allowReserved:e?.allowReserved||!1}));continue}n.push(V(r,i,e))}}return n.join(`&`)}}function at(e,t){let n=e;for(let r of e.match(ut)??[]){let e=r.substring(1,r.length-1),i=!1,a=`simple`;if(e.endsWith(`*`)&&(i=!0,e=e.substring(0,e.length-1)),e.startsWith(`.`)?(a=`label`,e=e.substring(1)):e.startsWith(`;`)&&(a=`matrix`,e=e.substring(1)),!t||t[e]===void 0||t[e]===null)continue;let o=t[e];if(Array.isArray(o)){n=n.replace(r,rt(e,o,{style:a,explode:i}));continue}if(typeof o==`object`){n=n.replace(r,nt(e,o,{style:a,explode:i}));continue}if(a===`matrix`){n=n.replace(r,`;${V(e,o)}`);continue}n=n.replace(r,a===`label`?`.${encodeURIComponent(o)}`:encodeURIComponent(o))}return n}function ot(e,t){return e instanceof FormData?e:t&&(t.get instanceof Function?t.get(`Content-Type`)??t.get(`content-type`):t[`Content-Type`]??t[`content-type`])===`application/x-www-form-urlencoded`?new URLSearchParams(e).toString():JSON.stringify(e)}function st(e,t){let n=`${t.baseUrl}${e}`;t.params?.path&&(n=t.pathSerializer(n,t.params.path));let r=t.querySerializer(t.params.query??{});return r.startsWith(`?`)&&(r=r.substring(1)),r&&(n+=`?${r}`),n}function ct(...e){let t=new Headers;for(let n of e){if(!n||typeof n!=`object`)continue;let e=n instanceof Headers?n.entries():Object.entries(n);for(let[n,r]of e)if(r===null)t.delete(n);else if(Array.isArray(r))for(let e of r)t.append(n,e);else r!==void 0&&t.set(n,r)}return t}function lt(e){return e.endsWith(`/`)?e.substring(0,e.length-1):e}var ut,dt;function ft(){return(ft=e((()=>{ut=/\{[^{}]+\}/g,dt=()=>typeof process==`object`&&Number.parseInt(process?.versions?.node?.substring(0,2))>=18&&process.versions.undici})))()}function pt(e){if(!e||typeof e!=`object`||Array.isArray(e))return{};let t=e,n=t.status===`error`&&t.details&&typeof t.details==`object`&&!Array.isArray(t.details)?t.details:t,r={};for(let[e,i]of Object.entries(n))if(!(n===t&&gt.has(e))){if(Array.isArray(i)){let t=i.filter(e=>typeof e==`string`);t.length>0&&(r[e]=t)}else typeof i==`string`&&(r[e]=[i])}return r}var H,mt,ht,gt;function _t(){return(_t=e((()=>{H=class extends Error{status;statusText;data;constructor(e,t,n){super(`HTTP ${e}: ${t}`),this.status=e,this.statusText=t,this.data=n,this.name=`HttpError`}},mt=class extends Error{cause;constructor(e){super(`Network request failed`),this.cause=e,this.name=`NetworkError`}},ht=class extends H{fieldErrors;constructor(e,t,n,r){super(e,t,n),this.fieldErrors=r,this.name=`ValidationError`}},gt=new Set([`detail`,`status`,`message`,`type`])})))()}function vt(){let e=document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);return e?decodeURIComponent(e[1]):``}function yt(){let e=encodeURIComponent(window.location.pathname+window.location.search);throw window.location.href=`/utilisateur/connexion?next=${e}`,Error(`Redirecting to login`)}function bt(e){let t=[`GET`,`POST`,`PUT`,`PATCH`,`DELETE`,`HEAD`,`OPTIONS`,`TRACE`],n={...e};for(let r of t){let t=e[r];n[r]=async(...e)=>{try{return await t(...e)}catch(e){throw e instanceof DOMException&&e.name===`AbortError`||e instanceof H||e instanceof Error&&e.message===`Redirecting to login`?e:new mt(e)}}}return n}var xt,St,U;function Ct(){return(Ct=e((()=>{ft(),_t(),xt={async onRequest({request:e}){if(e.method!==`GET`)return e.headers.set(`X-CSRFToken`,vt()),e}},St={async onResponse({response:e}){if(e.ok)return;e.status===401&&yt();let t=await e.clone().json().catch(()=>void 0);throw e.status===400||e.status===422?new ht(e.status,e.statusText,t,pt(t)):new H(e.status,e.statusText,t)}},U=tt({baseUrl:typeof window<`u`?window.location.origin:``,credentials:`same-origin`,fetch:(...e)=>globalThis.fetch(...e)}),U.use(xt),U.use(St),bt(U)})))()}function wt(){let e=document.createElement(`form`);e.method=`POST`,e.action=`/utilisateur/deconnexion`,e.hidden=!0;let t=document.createElement(`input`);t.type=`hidden`,t.name=`csrfmiddlewaretoken`,t.value=vt(),e.append(t),document.body.append(e),e.submit()}function Tt(){return(Tt=e((()=>{Ct()})))()}function Et(){return typeof window>`u`?!1:window.matchMedia(`(prefers-color-scheme: dark)`).matches}function W(e){typeof document>`u`||document.documentElement.setAttribute(`data-fr-theme`,e?`dark`:`light`)}function Dt(){let e=C(()=>K.value===`system`?q.value:K.value===`dark`);function t(t){K.value=t,localStorage.setItem(G,t),W(e.value)}function n(){t(e.value?`light`:`dark`)}let r=null,i=null;return l(()=>{q.value=Et();let t=localStorage.getItem(G);t&&[`light`,`dark`,`system`].includes(t)&&(K.value=t),W(e.value),r=window.matchMedia(`(prefers-color-scheme: dark)`),i=e=>{q.value=e.matches,K.value===`system`&&W(e.matches)},r.addEventListener(`change`,i)}),w(()=>{r&&i&&r.removeEventListener(`change`,i)}),c(e,e=>{W(e)}),{colorMode:K,isDark:e,setColorMode:t,toggle:n}}var G,K,q;function Ot(){return(Ot=e((()=>{g(),G=`csp_color_mode`,K=v(`system`),q=v(!1)})))()}var kt,At,jt,Mt;function Nt(){return(Nt=e((()=>{g(),Tt(),te(),M(),T(),Ot(),R(),kt={key:0,class:`csp-sidebar-user__info`,"data-testid":`sidebar-user-info`},At={class:`csp-sidebar-user__name`},jt={key:0,class:`csp-sidebar-user__role`},Mt=n({__name:`CspSidebarUser`,props:{name:{},role:{}},setup(e){let{isExpanded:n,isMobile:a}=P(),{isDark:o,toggle:s}=Dt();return(c,l)=>(d(),x(ne,{side:`right`,align:`end`,sections:[{items:[{label:S(o)?`Mode clair`:`Mode sombre`,icon:S(o)?`ri:sun-line`:`ri:moon-line`,onSelect:S(s)}]},{items:[{label:`Mon profil`,icon:`ri:user-line`},{label:`Paramètres`,icon:`ri:settings-3-line`}]},{items:[{label:`Se déconnecter`,icon:`ri:logout-box-r-line`,destructive:!0,onSelect:S(wt)}]}]},{trigger:y(()=>[h(`button`,{type:`button`,class:b([`csp-sidebar-user`,{"csp-sidebar-user--expanded":S(n)||S(a)}])},[i(k,{name:e.name,size:`md`},null,8,[`name`]),S(n)||S(a)?(d(),t(`div`,kt,[h(`span`,At,r(e.name),1),e.role?(d(),t(`span`,jt,r(e.role),1)):u(``,!0)])):u(``,!0),S(n)||S(a)?(d(),x(E,{key:1,name:`ri:expand-up-down-line`,size:16,class:`csp-sidebar-user__chevron`})):u(``,!0)],2)]),_:1},8,[`sections`]))}})})))()}var Pt;function Ft(){return(Ft=e((()=>{Nt(),D(),Pt=O(Mt,[[`__scopeId`,`data-v-4d3828b4`]])})))()}var It,J,Y,X,Z,Q,$,Lt;function Rt(){return(Rt=e((()=>{m(),Ae(),Fe(),Be(),Ke(),Ye(),$e(),Ft(),It={title:`Compositions/Génériques/CspSidebar`,component:B,parameters:{layout:`fullscreen`,docs:{description:{component:'\nSidebar de navigation adaptée au DSFR.\n\n## Composants\n\n- `CspSidebarProvider` : contexte partagé (état, mobile, raccourcis)\n- `CspSidebar` : panneau de navigation\n- `CspSidebarTrigger` : bouton hamburger mobile (dans le header)\n- `CspSidebarGroup`, `CspSidebarItem`, `CspSidebarLogo`, `CspSidebarUser`\n\n## Usage\n\n```vue\n<CspAppShell :navigation="navigation">\n  <!-- contenu de page -->\n</CspAppShell>\n```\n        '}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},J=`
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
`,Y={CspSidebar:ke,CspSidebarGroup:Pe,CspSidebarItem:ze,CspSidebarLogo:Ge,CspSidebarProvider:B,CspSidebarTrigger:Qe,CspSidebarUser:Pt},X={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Z={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Q={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},$={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:Y,setup(){let t=ee();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
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