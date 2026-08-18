import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,E as r,H as i,M as a,Q as o,R as s,S as c,St as l,Tt as u,V as d,W as f,Z as p,a as m,b as h,c as g,ft as _,i as v,s as y,tt as b,wt as x,x as S,y as C,yt as w,z as T}from"./iframe-CrUhtth-.js";import{n as E,t as D}from"./CspIcon-D2nV9hNu.js";import{n as O,t as k}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as ee,t as A}from"./CspAvatar-DsqFmZEc.js";import{n as j,t as M}from"./Primitive-Ba3BVjgw.js";import{n as N,t as te}from"./CspDropdownMenu-DvTzdgKW.js";import{n as P,t as ne}from"./CspTooltip-CadvUxK0.js";import{a as re,c as ie,i as ae,n as oe,o as se,r as ce,s as le,t as ue}from"./DialogPortal-DQcMIh2c.js";import{n as de,t as fe}from"./CspButton-DWH4jZfL.js";function pe(e){let t=_(!1);function n(){typeof window<`u`&&(t.value=window.innerWidth<=e)}return s(()=>{n(),window.addEventListener(`resize`,n)}),T(()=>{window.removeEventListener(`resize`,n)}),t}function me(e){let{defaultExpanded:t=!0,persistState:n=!0}=e,r=localStorage.getItem(I),a=_(r===null?t:r===`true`),c=pe(768),l=_(!1),u=C(()=>a.value?`expanded`:`collapsed`);function d(e){a.value=e,n&&localStorage.setItem(I,String(e))}function f(e){l.value=e}function p(){c.value?f(!l.value):d(!a.value)}function m(e){e.key===`b`&&(e.metaKey||e.ctrlKey)&&(e.preventDefault(),p())}s(()=>{window.addEventListener(`keydown`,m)}),T(()=>{window.removeEventListener(`keydown`,m)}),o(c,e=>{!e&&l.value&&(l.value=!1)});let h={state:u,isExpanded:a,isMobile:c,isMobileOpen:l,setExpanded:d,setMobileOpen:f,toggle:p};return i(R,h),h}function F(){let e=a(R);if(!e)throw Error(`useSidebar must be used within a CspSidebar provider`);return e}var I,L,he,R;function z(){return(z=e((()=>{g(),I=`csp_sidebar_state`,L=`15rem`,he=`4rem`,R=Symbol(`sidebar`)})))()}var ge,_e,ve,ye,be,xe,Se,Ce,we,Te,Ee;function De(){return(De=e((()=>{g(),se(),ae(),oe(),ie(),de(),E(),z(),ge={class:`csp-sidebar__header`},_e={key:0,class:`csp-sidebar__brand`},ve={class:`csp-sidebar__nav`},ye={key:0,class:`csp-sidebar__footer`},be=[`data-state`,`aria-expanded`],xe={class:`csp-sidebar__header`},Se={key:0,class:`csp-sidebar__brand`},Ce=[`aria-label`,`title`],we={class:`csp-sidebar__nav`},Te={key:0,class:`csp-sidebar__footer`},Ee=n({__name:`CspSidebar`,setup(e){let n=p(),i=C(()=>!!n.logo),a=C(()=>!!n.footer),{state:o,isExpanded:s,isMobile:u,isMobileOpen:m,setMobileOpen:g,toggle:_}=F();return(e,n)=>w(u)?(d(),S(w(le),{key:0,open:w(m),"onUpdate:open":w(g)},{default:b(()=>[r(w(ue),null,{default:b(()=>[r(w(ce),{class:`csp-sidebar-overlay`}),r(w(re),{class:`csp-sidebar csp-sidebar--mobile`,"aria-label":e.$attrs[`aria-label`]??`Menu de navigation`,style:x({"--sidebar-width":w(L)})},{default:b(()=>[h(`header`,ge,[i.value?(d(),t(`div`,_e,[f(e.$slots,`logo`,{},void 0,!0)])):c(``,!0),r(fe,{class:`csp-sidebar__close`,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":`Fermer le menu`,onClick:n[0]||=e=>w(g)(!1)})]),h(`nav`,ve,[f(e.$slots,`default`,{},void 0,!0)]),a.value?(d(),t(`div`,ye,[f(e.$slots,`footer`,{},void 0,!0)])):c(``,!0)]),_:3},8,[`aria-label`,`style`])]),_:3})]),_:3},8,[`open`,`onUpdate:open`])):(d(),t(`nav`,{key:1,class:l([`csp-sidebar`,{"csp-sidebar--expanded":w(s)}]),"data-state":w(o),"aria-expanded":w(s),style:x({"--sidebar-width":w(L),"--sidebar-width-collapsed":w(he)})},[h(`div`,xe,[i.value&&w(s)?(d(),t(`div`,Se,[f(e.$slots,`logo`,{},void 0,!0)])):c(``,!0),h(`button`,{type:`button`,class:`csp-sidebar__toggle`,"aria-label":w(s)?`Réduire le menu`:`Ouvrir le menu`,title:`${w(s)?`Réduire`:`Ouvrir`} (Ctrl+B)`,onClick:n[1]||=(...e)=>w(_)&&w(_)(...e)},[r(D,{name:w(s)?`ri:sidebar-fold-line`:`ri:sidebar-unfold-line`,size:18},null,8,[`name`])],8,Ce)]),h(`div`,we,[f(e.$slots,`default`,{},void 0,!0)]),a.value?(d(),t(`div`,Te,[f(e.$slots,`footer`,{},void 0,!0)])):c(``,!0)],14,be))}})})))()}var Oe;function ke(){return(ke=e((()=>{De(),O(),Oe=k(Ee,[[`__scopeId`,`data-v-40fc1d50`]])})))()}var Ae,je,Me,Ne;function Pe(){return(Pe=e((()=>{g(),z(),Ae=[`aria-label`],je={key:0,class:`csp-sidebar-group__label`},Me={class:`csp-sidebar-group__items`},Ne=n({__name:`CspSidebarGroup`,props:{label:{}},setup(e){let{isExpanded:n,isMobile:r}=F();return(i,a)=>(d(),t(`div`,{class:`csp-sidebar-group`,role:`group`,"aria-label":e.label},[w(n)||w(r)?(d(),t(`span`,je,u(e.label),1)):c(``,!0),h(`div`,Me,[f(i.$slots,`default`,{},void 0,!0)])],8,Ae))}})})))()}var Fe;function Ie(){return(Ie=e((()=>{Pe(),O(),Fe=k(Ne,[[`__scopeId`,`data-v-d9981547`]])})))()}var Le,Re;function ze(){return(ze=e((()=>{g(),j(),m(),E(),P(),z(),Le={key:0,class:`csp-sidebar-item__label`},Re=n({inheritAttrs:!1,__name:`CspSidebarItem`,props:{icon:{},label:{},to:{},isActive:{type:Boolean,default:!1}},setup(e){let{isExpanded:n,isMobile:i}=F();return(a,o)=>(d(),S(ne,{content:e.label,disabled:w(n)||w(i),side:`right`,"side-offset":12},{default:b(()=>[r(w(M),{as:e.to?w(v):`button`,to:e.to,type:e.to?void 0:`button`,class:l([`csp-sidebar-item`,{"csp-sidebar-item--active":e.isActive,"csp-sidebar-item--expanded":w(n)||w(i)}]),"aria-current":e.isActive?`page`:void 0},{default:b(()=>[r(D,{class:`csp-sidebar-item__icon`,name:e.icon,size:16},null,8,[`name`]),w(n)||w(i)?(d(),t(`span`,Le,u(e.label),1)):c(``,!0)]),_:1},8,[`as`,`to`,`type`,`class`,`aria-current`])]),_:1},8,[`content`,`disabled`]))}})})))()}var Be;function Ve(){return(Ve=e((()=>{ze(),O(),Be=k(Re,[[`__scopeId`,`data-v-d69b2512`]])})))()}var He,Ue,We;function Ge(){return(Ge=e((()=>{g(),z(),He={class:`csp-sidebar-logo`},Ue={key:0,class:`csp-sidebar-logo__subtitle`},We=n({__name:`CspSidebarLogo`,setup(e){let{isExpanded:n,isMobile:r}=F();return(e,i)=>(d(),t(`div`,He,[i[0]||=h(`span`,{class:`csp-sidebar-logo__title`},`CSPLab`,-1),w(n)||w(r)?(d(),t(`span`,Ue,` ATS `)):c(``,!0)]))}})})))()}var Ke;function qe(){return(qe=e((()=>{Ge(),O(),Ke=k(We,[[`__scopeId`,`data-v-8492f1ff`]])})))()}var Je;function Ye(){return(Ye=e((()=>{g(),z(),Je=n({__name:`CspSidebarProvider`,props:{defaultExpanded:{type:Boolean,default:!0},persistState:{type:Boolean,default:!0}},setup(e){let t=e;return me({defaultExpanded:t.defaultExpanded,persistState:t.persistState}),(e,t)=>f(e.$slots,`default`)}})})))()}var B;function Xe(){return(Xe=e((()=>{Ye(),B=Je})))()}var Ze;function Qe(){return(Qe=e((()=>{g(),de(),z(),Ze=n({__name:`CspSidebarTrigger`,setup(e){let{toggle:t,isMobile:n}=F();return(e,r)=>w(n)?(d(),S(fe,{key:0,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:menu-line`,"aria-label":`Ouvrir le menu`,onClick:w(t)},null,8,[`onClick`])):c(``,!0)}})})))()}var $e;function et(){return(et=e((()=>{Qe(),$e=Ze})))()}function tt(){return Math.random().toString(36).slice(2,11)}function nt(e){let{baseUrl:t=``,Request:n=globalThis.Request,fetch:r=globalThis.fetch,querySerializer:i,bodySerializer:a,pathSerializer:o,headers:s,requestInitExt:c=void 0,...l}={...e};c=ft()?c:void 0,t=ut(t);let u=[];async function d(e,d){let{baseUrl:f,fetch:p=r,Request:m=n,headers:h,params:g={},parseAs:_=`json`,querySerializer:v,bodySerializer:y=a??st,pathSerializer:b,body:x,middleware:S=[],...C}=d||{},w=t;f&&(w=ut(f)??t);let T=typeof i==`function`?i:at(i);v&&(T=typeof v==`function`?v:at({...typeof i==`object`?i:{},...v}));let E=b||o||ot,D=x===void 0?void 0:y(x,lt(s,h,g.header)),O=lt(D===void 0||D instanceof FormData?{}:{"Content-Type":`application/json`},s,h,g.header),k=[...u,...S],ee={redirect:`follow`,...l,...C,body:D,headers:O},A,j,M=new m(ct(e,{baseUrl:w,params:g,querySerializer:T,pathSerializer:E}),ee),N;for(let e in C)e in M||(M[e]=C[e]);if(k.length){A=tt(),j=Object.freeze({baseUrl:w,fetch:p,parseAs:_,querySerializer:T,bodySerializer:y,pathSerializer:E});for(let t of k)if(t&&typeof t==`object`&&typeof t.onRequest==`function`){let n=await t.onRequest({request:M,schemaPath:e,params:g,options:j,id:A});if(n){if(n instanceof m)M=n;else if(n instanceof Response){N=n;break}else throw Error(`onRequest: must return new Request() or Response() when modifying the request`)}}}if(!N){try{N=await p(M,c)}catch(t){let n=t;if(k.length)for(let t=k.length-1;t>=0;t--){let r=k[t];if(r&&typeof r==`object`&&typeof r.onError==`function`){let t=await r.onError({request:M,error:n,schemaPath:e,params:g,options:j,id:A});if(t){if(t instanceof Response){n=void 0,N=t;break}if(t instanceof Error){n=t;continue}throw Error(`onError: must return new Response() or instance of Error`)}}}if(n)throw n}if(k.length)for(let t=k.length-1;t>=0;t--){let n=k[t];if(n&&typeof n==`object`&&typeof n.onResponse==`function`){let t=await n.onResponse({request:M,response:N,schemaPath:e,params:g,options:j,id:A});if(t){if(!(t instanceof Response))throw Error(`onResponse: must return new Response() when modifying the response`);N=t}}}}let te=N.headers.get(`Content-Length`);if(N.status===204||M.method===`HEAD`||te===`0`&&!N.headers.get(`Transfer-Encoding`)?.includes(`chunked`))return N.ok?{data:void 0,response:N}:{error:void 0,response:N};if(N.ok)return{data:await(async()=>{if(_===`stream`)return N.body;if(_===`json`&&!te){let e=await N.text();return e?JSON.parse(e):void 0}return await N[_]()})(),response:N};let P=await N.text();try{P=JSON.parse(P)}catch{}return{error:P,response:N}}return{request(e,t,n){return d(t,{...n,method:e.toUpperCase()})},GET(e,t){return d(e,{...t,method:`GET`})},PUT(e,t){return d(e,{...t,method:`PUT`})},POST(e,t){return d(e,{...t,method:`POST`})},DELETE(e,t){return d(e,{...t,method:`DELETE`})},OPTIONS(e,t){return d(e,{...t,method:`OPTIONS`})},HEAD(e,t){return d(e,{...t,method:`HEAD`})},PATCH(e,t){return d(e,{...t,method:`PATCH`})},TRACE(e,t){return d(e,{...t,method:`TRACE`})},use(...e){for(let t of e)if(t){if(typeof t!=`object`||!(`onRequest`in t||`onResponse`in t||`onError`in t))throw Error("Middleware must be an object with one of `onRequest()`, `onResponse() or `onError()`");u.push(t)}},eject(...e){for(let t of e){let e=u.indexOf(t);e!==-1&&u.splice(e,1)}}}}function V(e,t,n){if(t==null)return``;if(typeof t==`object`)throw Error("Deeply-nested arrays/objects aren’t supported. Provide your own `querySerializer()` to handle these.");return`${e}=${n?.allowReserved===!0?t:encodeURIComponent(t)}`}function rt(e,t,n){if(!t||typeof t!=`object`)return``;let r=[],i={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`;if(n.style!==`deepObject`&&n.explode===!1){for(let e in t)r.push(e,n.allowReserved===!0?t[e]:encodeURIComponent(t[e]));let i=r.join(`,`);switch(n.style){case`form`:return`${e}=${i}`;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return i}}for(let i in t){let a=n.style===`deepObject`?`${e}[${i}]`:i;r.push(V(a,t[i],n))}let a=r.join(i);return n.style===`label`||n.style===`matrix`?`${i}${a}`:a}function it(e,t,n){if(!Array.isArray(t))return``;if(n.explode===!1){let r={form:`,`,spaceDelimited:`%20`,pipeDelimited:`|`}[n.style]||`,`,i=(n.allowReserved===!0?t:t.map(e=>encodeURIComponent(e))).join(r);switch(n.style){case`simple`:return i;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return`${e}=${i}`}}let r={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`,i=[];for(let r of t)n.style===`simple`||n.style===`label`?i.push(n.allowReserved===!0?r:encodeURIComponent(r)):i.push(V(e,r,n));return n.style===`label`||n.style===`matrix`?`${r}${i.join(r)}`:i.join(r)}function at(e){return function(t){let n=[];if(t&&typeof t==`object`)for(let r in t){let i=t[r];if(i!=null){if(Array.isArray(i)){if(i.length===0)continue;n.push(it(r,i,{style:`form`,explode:!0,...e?.array,allowReserved:e?.allowReserved||!1}));continue}if(typeof i==`object`){n.push(rt(r,i,{style:`deepObject`,explode:!0,...e?.object,allowReserved:e?.allowReserved||!1}));continue}n.push(V(r,i,e))}}return n.join(`&`)}}function ot(e,t){let n=e;for(let r of e.match(dt)??[]){let e=r.substring(1,r.length-1),i=!1,a=`simple`;if(e.endsWith(`*`)&&(i=!0,e=e.substring(0,e.length-1)),e.startsWith(`.`)?(a=`label`,e=e.substring(1)):e.startsWith(`;`)&&(a=`matrix`,e=e.substring(1)),!t||t[e]===void 0||t[e]===null)continue;let o=t[e];if(Array.isArray(o)){n=n.replace(r,it(e,o,{style:a,explode:i}));continue}if(typeof o==`object`){n=n.replace(r,rt(e,o,{style:a,explode:i}));continue}if(a===`matrix`){n=n.replace(r,`;${V(e,o)}`);continue}n=n.replace(r,a===`label`?`.${encodeURIComponent(o)}`:encodeURIComponent(o))}return n}function st(e,t){return e instanceof FormData?e:t&&(t.get instanceof Function?t.get(`Content-Type`)??t.get(`content-type`):t[`Content-Type`]??t[`content-type`])===`application/x-www-form-urlencoded`?new URLSearchParams(e).toString():JSON.stringify(e)}function ct(e,t){let n=`${t.baseUrl}${e}`;t.params?.path&&(n=t.pathSerializer(n,t.params.path));let r=t.querySerializer(t.params.query??{});return r.startsWith(`?`)&&(r=r.substring(1)),r&&(n+=`?${r}`),n}function lt(...e){let t=new Headers;for(let n of e){if(!n||typeof n!=`object`)continue;let e=n instanceof Headers?n.entries():Object.entries(n);for(let[n,r]of e)if(r===null)t.delete(n);else if(Array.isArray(r))for(let e of r)t.append(n,e);else r!==void 0&&t.set(n,r)}return t}function ut(e){return e.endsWith(`/`)?e.substring(0,e.length-1):e}var dt,ft;function pt(){return(pt=e((()=>{dt=/\{[^{}]+\}/g,ft=()=>typeof process==`object`&&Number.parseInt(process?.versions?.node?.substring(0,2))>=18&&process.versions.undici})))()}function mt(e){if(!e||typeof e!=`object`||Array.isArray(e))return{};let t=e,n=t.status===`error`&&t.details&&typeof t.details==`object`&&!Array.isArray(t.details)?t.details:t,r={};for(let[e,i]of Object.entries(n))if(!(n===t&&_t.has(e))){if(Array.isArray(i)){let t=i.filter(e=>typeof e==`string`);t.length>0&&(r[e]=t)}else typeof i==`string`&&(r[e]=[i])}return r}var H,ht,gt,_t;function vt(){return(vt=e((()=>{H=class extends Error{status;statusText;data;constructor(e,t,n){super(`HTTP ${e}: ${t}`),this.status=e,this.statusText=t,this.data=n,this.name=`HttpError`}},ht=class extends Error{cause;constructor(e){super(`Network request failed`),this.cause=e,this.name=`NetworkError`}},gt=class extends H{fieldErrors;constructor(e,t,n,r){super(e,t,n),this.fieldErrors=r,this.name=`ValidationError`}},_t=new Set([`detail`,`status`,`message`,`type`])})))()}function yt(){let e=document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);return e?decodeURIComponent(e[1]):``}function bt(){let e=encodeURIComponent(window.location.pathname+window.location.search);throw window.location.href=`/utilisateur/connexion?next=${e}`,Error(`Redirecting to login`)}function xt(e){let t=[`GET`,`POST`,`PUT`,`PATCH`,`DELETE`,`HEAD`,`OPTIONS`,`TRACE`],n={...e};for(let r of t){let t=e[r];n[r]=async(...e)=>{try{return await t(...e)}catch(e){throw e instanceof DOMException&&e.name===`AbortError`||e instanceof H||e instanceof Error&&e.message===`Redirecting to login`?e:new ht(e)}}}return n}var St,Ct,U;function wt(){return(wt=e((()=>{pt(),vt(),St={async onRequest({request:e}){if(e.method!==`GET`)return e.headers.set(`X-CSRFToken`,yt()),e}},Ct={async onResponse({response:e}){if(e.ok)return;e.status===401&&bt();let t=await e.clone().json().catch(()=>void 0);throw e.status===400||e.status===422?new gt(e.status,e.statusText,t,mt(t)):new H(e.status,e.statusText,t)}},U=nt({baseUrl:typeof window<`u`?window.location.origin:``,credentials:`same-origin`,fetch:(...e)=>globalThis.fetch(...e)}),U.use(St),U.use(Ct),xt(U)})))()}async function Tt(){await fetch(`/utilisateur/deconnexion`,{method:`POST`,credentials:`same-origin`,headers:{"X-CSRFToken":yt()}}),window.location.href=`/`}function Et(){return(Et=e((()=>{wt()})))()}function Dt(){return typeof window>`u`?!1:window.matchMedia(`(prefers-color-scheme: dark)`).matches}function W(e){typeof document>`u`||document.documentElement.setAttribute(`data-fr-theme`,e?`dark`:`light`)}function Ot(){let e=C(()=>K.value===`system`?q.value:K.value===`dark`);function t(t){K.value=t,localStorage.setItem(G,t),W(e.value)}function n(){t(e.value?`light`:`dark`)}let r=null,i=null;return s(()=>{q.value=Dt();let t=localStorage.getItem(G);t&&[`light`,`dark`,`system`].includes(t)&&(K.value=t),W(e.value),r=window.matchMedia(`(prefers-color-scheme: dark)`),i=e=>{q.value=e.matches,K.value===`system`&&W(e.matches)},r.addEventListener(`change`,i)}),T(()=>{r&&i&&r.removeEventListener(`change`,i)}),o(e,e=>{W(e)}),{colorMode:K,isDark:e,setColorMode:t,toggle:n}}var G,K,q;function kt(){return(kt=e((()=>{g(),G=`csp_color_mode`,K=_(`system`),q=_(!1)})))()}var At,jt,Mt,Nt;function Pt(){return(Pt=e((()=>{g(),Et(),ee(),N(),E(),kt(),z(),At={key:0,class:`csp-sidebar-user__info`},jt={class:`csp-sidebar-user__name`},Mt={key:0,class:`csp-sidebar-user__role`},Nt=n({__name:`CspSidebarUser`,props:{name:{},role:{}},setup(e){let{isExpanded:n,isMobile:i}=F(),{isDark:a,toggle:o}=Ot();return(s,f)=>(d(),S(te,{side:`right`,align:`end`,sections:[{items:[{label:w(a)?`Mode clair`:`Mode sombre`,icon:w(a)?`ri:sun-line`:`ri:moon-line`,onSelect:w(o)}]},{items:[{label:`Mon profil`,icon:`ri:user-line`},{label:`Paramètres`,icon:`ri:settings-3-line`}]},{items:[{label:`Se déconnecter`,icon:`ri:logout-box-r-line`,destructive:!0,onSelect:w(Tt)}]}]},{trigger:b(()=>[h(`button`,{type:`button`,class:l([`csp-sidebar-user`,{"csp-sidebar-user--expanded":w(n)||w(i)}])},[r(A,{name:e.name,size:`md`},null,8,[`name`]),w(n)||w(i)?(d(),t(`div`,At,[h(`span`,jt,u(e.name),1),e.role?(d(),t(`span`,Mt,u(e.role),1)):c(``,!0)])):c(``,!0),w(n)||w(i)?(d(),S(D,{key:1,name:`ri:expand-up-down-line`,size:16,class:`csp-sidebar-user__chevron`})):c(``,!0)],2)]),_:1},8,[`sections`]))}})})))()}var Ft;function It(){return(It=e((()=>{Pt(),O(),Ft=k(Nt,[[`__scopeId`,`data-v-eb144a6d`]])})))()}var Lt,J,Y,X,Z,Q,$,Rt;function zt(){return(zt=e((()=>{m(),ke(),Ie(),Ve(),qe(),Xe(),et(),It(),Lt={title:`Compositions/Génériques/CspSidebar`,component:B,parameters:{layout:`fullscreen`,docs:{description:{component:'\nSidebar de navigation adaptée au DSFR.\n\n## Composants\n\n- `CspSidebarProvider` : contexte partagé (état, mobile, raccourcis)\n- `CspSidebar` : panneau de navigation\n- `CspSidebarTrigger` : bouton hamburger mobile (dans le header)\n- `CspSidebarGroup`, `CspSidebarItem`, `CspSidebarLogo`, `CspSidebarUser`\n\n## Usage\n\n```vue\n<CspAppShell :navigation="navigation">\n  <!-- contenu de page -->\n</CspAppShell>\n```\n        '}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},J=`
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
`,Y={CspSidebar:Oe,CspSidebarGroup:Fe,CspSidebarItem:Be,CspSidebarLogo:Ke,CspSidebarProvider:B,CspSidebarTrigger:$e,CspSidebarUser:Ft},X={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Z={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Q={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},$={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:Y,setup(){let t=y();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
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
}`,...$.parameters?.docs?.source}}},Rt=[`Default`,`Collapsed`,`Mobile`,`WithRouterLinks`]})))()}zt();export{Z as Collapsed,X as Default,Q as Mobile,$ as WithRouterLinks,Rt as __namedExportsOrder,Lt as default};