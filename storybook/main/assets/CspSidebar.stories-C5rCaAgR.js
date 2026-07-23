import{i as e}from"./preload-helper-Ct_ODC0V.js";import{At as t,B as n,Bt as r,D as i,G as a,H as o,Ht as s,K as c,Lt as l,R as u,Ut as d,V as f,Z as p,gt as m,ht as h,i as g,it as _,lt as v,o as y,ot as b,r as ee,rt as x,st as te,yt as S,z as C}from"./iframe-8DGZZ6On.js";import{n as ne,t as w}from"./CspAvatar-DeLEjK1S.js";import{n as T,t as E}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as D,t as O}from"./CspIcon-BMBm_gp1.js";import{En as k,On as A,Sn as j,gn as re,t as M,vn as ie}from"./dist-pnSe46cx.js";import{n as ae,t as oe}from"./CspButton-DOTuhIJV.js";import{n as se,t as ce}from"./CspDropdownMenu-C3kmk2BP.js";import{n as le,t as ue}from"./CspTooltip-CT8ZAIO-.js";var de,fe,pe,me,he,N,ge=e((()=>{i(),de={class:`csp-app-layout`},fe={class:`csp-app-layout__sidebar`},pe={class:`csp-app-layout__content`},me={key:0,class:`csp-app-layout__header`},he={class:`csp-app-layout__main`},N=c({__name:`CspAppLayout`,setup(e){let t=h(),n=u(()=>!!t.header);return(e,t)=>(b(),o(`div`,de,[C(`aside`,fe,[v(e.$slots,`sidebar`,{},void 0,!0)]),C(`div`,pe,[n.value?(b(),o(`header`,me,[v(e.$slots,`header`,{},void 0,!0)])):f(``,!0),C(`main`,he,[v(e.$slots,`default`,{},void 0,!0)])])]))}})})),_e=e((()=>{})),ve,ye=e((()=>{ge(),ge(),_e(),T(),ve=E(N,[[`__scopeId`,`data-v-8ce26768`]]),N.__docgenInfo=Object.assign({displayName:N.name??N.__name},{exportName:`default`,displayName:`CspAppLayout`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`sidebar`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`header`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspAppLayout/CspAppLayout.vue`})}));function be(e){let n=t(!1);function r(){typeof window<`u`&&(n.value=window.innerWidth<=e)}return x(()=>{r(),window.addEventListener(`resize`,r)}),_(()=>{window.removeEventListener(`resize`,r)}),n}function xe(e){let{defaultExpanded:n=!0,persistState:r=!0}=e,i=localStorage.getItem(Se),a=t(i===null?n:i===`true`),o=be(768),s=t(!1),c=u(()=>a.value?`expanded`:`collapsed`);function l(e){a.value=e,r&&localStorage.setItem(Se,String(e))}function d(e){s.value=e}function f(){o.value?d(!s.value):l(!a.value)}function p(e){e.key===`b`&&(e.metaKey||e.ctrlKey)&&(e.preventDefault(),f())}x(()=>{window.addEventListener(`keydown`,p)}),_(()=>{window.removeEventListener(`keydown`,p)}),m(o,e=>{!e&&s.value&&(s.value=!1)});let h={state:c,isExpanded:a,isMobile:o,isMobileOpen:s,setExpanded:l,setMobileOpen:d,toggle:f};return te(Te,h),h}function P(){let e=p(Te);if(!e)throw Error(`useSidebar must be used within a CspSidebar provider`);return e}var Se,Ce,we,Te,F=e((()=>{i(),Se=`csp_sidebar_state`,Ce=`15rem`,we=`4rem`,Te=Symbol(`sidebar`),xe.__docgenInfo=Object.assign({displayName:xe.name??xe.__name},{exportName:`provideSidebar`,displayName:`provideSidebar`,type:2,props:[{name:`defaultExpanded`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`persistState`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/composables/ui/useSidebar.ts`})})),Ee,De,Oe,ke,Ae,je,Me,Ne,Pe,Fe,I,Ie=e((()=>{i(),M(),ae(),D(),F(),Ee={class:`csp-sidebar__header`},De={key:0,class:`csp-sidebar__brand`},Oe={class:`csp-sidebar__nav`},ke={key:0,class:`csp-sidebar__footer`},Ae=[`data-state`,`aria-expanded`],je={class:`csp-sidebar__header`},Me={key:0,class:`csp-sidebar__brand`},Ne=[`aria-label`,`title`],Pe={class:`csp-sidebar__nav`},Fe={key:0,class:`csp-sidebar__footer`},I=c({__name:`CspSidebar`,setup(e){let t=h(),i=u(()=>!!t.logo),c=u(()=>!!t.footer),{state:d,isExpanded:p,isMobile:m,isMobileOpen:g,setMobileOpen:_,toggle:y}=P();return(e,t)=>l(m)?(b(),n(l(k),{key:0,open:l(g),"onUpdate:open":l(_)},{default:S(()=>[a(l(re),null,{default:S(()=>[a(l(ie),{class:`csp-sidebar-overlay`}),a(l(j),{class:`csp-sidebar csp-sidebar--mobile`,"aria-label":e.$attrs[`aria-label`]??`Menu de navigation`,style:s({"--sidebar-width":l(Ce)})},{default:S(()=>[C(`header`,Ee,[i.value?(b(),o(`div`,De,[v(e.$slots,`logo`,{},void 0,!0)])):f(``,!0),a(oe,{class:`csp-sidebar__close`,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":`Fermer le menu`,onClick:t[0]||=e=>l(_)(!1)})]),C(`nav`,Oe,[v(e.$slots,`default`,{},void 0,!0)]),c.value?(b(),o(`div`,ke,[v(e.$slots,`footer`,{},void 0,!0)])):f(``,!0)]),_:3},8,[`aria-label`,`style`])]),_:3})]),_:3},8,[`open`,`onUpdate:open`])):(b(),o(`nav`,{key:1,class:r([`csp-sidebar`,{"csp-sidebar--expanded":l(p)}]),"data-state":l(d),"aria-expanded":l(p),style:s({"--sidebar-width":l(Ce),"--sidebar-width-collapsed":l(we)})},[C(`div`,je,[i.value&&l(p)?(b(),o(`div`,Me,[v(e.$slots,`logo`,{},void 0,!0)])):f(``,!0),C(`button`,{type:`button`,class:`csp-sidebar__toggle`,"aria-label":l(p)?`Réduire le menu`:`Ouvrir le menu`,title:`${l(p)?`Réduire`:`Ouvrir`} (Ctrl+B)`,onClick:t[1]||=(...e)=>l(y)&&l(y)(...e)},[a(O,{name:l(p)?`ri:sidebar-fold-line`:`ri:sidebar-unfold-line`,size:18},null,8,[`name`])],8,Ne)]),C(`div`,Pe,[v(e.$slots,`default`,{},void 0,!0)]),c.value?(b(),o(`div`,Fe,[v(e.$slots,`footer`,{},void 0,!0)])):f(``,!0)],14,Ae))}})})),Le=e((()=>{})),Re,ze=e((()=>{Ie(),Ie(),Le(),T(),Re=E(I,[[`__scopeId`,`data-v-c9f5c6bf`]]),I.__docgenInfo=Object.assign({displayName:I.name??I.__name},{exportName:`default`,displayName:`CspSidebar`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`logo`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`footer`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebar.vue`})})),Be,Ve,He,L,Ue=e((()=>{i(),F(),Be=[`aria-label`],Ve={key:0,class:`csp-sidebar-group__label`},He={class:`csp-sidebar-group__items`},L=c({__name:`CspSidebarGroup`,props:{label:{}},setup(e){let{isExpanded:t,isMobile:n}=P();return(r,i)=>(b(),o(`div`,{class:`csp-sidebar-group`,role:`group`,"aria-label":e.label},[l(t)||l(n)?(b(),o(`span`,Ve,d(e.label),1)):f(``,!0),C(`div`,He,[v(r.$slots,`default`,{},void 0,!0)])],8,Be))}})})),We=e((()=>{})),Ge,Ke=e((()=>{Ue(),Ue(),We(),T(),Ge=E(L,[[`__scopeId`,`data-v-d9981547`]]),L.__docgenInfo=Object.assign({displayName:L.name??L.__name},{exportName:`default`,displayName:`CspSidebarGroup`,type:1,props:[{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`label`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarGroup.vue`})})),qe,R,Je=e((()=>{i(),M(),g(),D(),le(),F(),qe={key:0,class:`csp-sidebar-item__label`},R=c({inheritAttrs:!1,__name:`CspSidebarItem`,props:{icon:{},label:{},to:{},isActive:{type:Boolean,default:!1}},setup(e){let{isExpanded:t,isMobile:i}=P();return(s,c)=>(b(),n(ue,{content:e.label,disabled:l(t)||l(i),side:`right`,"side-offset":12},{default:S(()=>[a(l(A),{as:e.to?l(ee):`button`,to:e.to,type:e.to?void 0:`button`,class:r([`csp-sidebar-item`,{"csp-sidebar-item--active":e.isActive,"csp-sidebar-item--expanded":l(t)||l(i)}]),"aria-current":e.isActive?`page`:void 0},{default:S(()=>[a(O,{class:`csp-sidebar-item__icon`,name:e.icon,size:16},null,8,[`name`]),l(t)||l(i)?(b(),o(`span`,qe,d(e.label),1)):f(``,!0)]),_:1},8,[`as`,`to`,`type`,`class`,`aria-current`])]),_:1},8,[`content`,`disabled`]))}})})),Ye=e((()=>{})),Xe,Ze=e((()=>{Je(),Je(),Ye(),T(),Xe=E(R,[[`__scopeId`,`data-v-d754f4f6`]]),R.__docgenInfo=Object.assign({displayName:R.name??R.__name},{exportName:`default`,displayName:`CspSidebarItem`,type:1,props:[{name:`icon`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`to`,global:!1,description:``,tags:[],required:!1,type:`any`,declarations:[],schema:`any`},{name:`isActive`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`isActive`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`icon`,type:`string`,description:``,declarations:[],schema:`string`},{name:`to`,type:`any`,description:``,declarations:[],schema:`any`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarItem.vue`})})),Qe,$e,z,et=e((()=>{i(),F(),Qe={class:`csp-sidebar-logo`},$e={key:0,class:`csp-sidebar-logo__subtitle`},z=c({__name:`CspSidebarLogo`,setup(e){let{isExpanded:t,isMobile:n}=P();return(e,r)=>(b(),o(`div`,Qe,[r[0]||=C(`span`,{class:`csp-sidebar-logo__title`},`CSPLab`,-1),l(t)||l(n)?(b(),o(`span`,$e,` ATS `)):f(``,!0)]))}})})),tt=e((()=>{})),nt,rt=e((()=>{et(),et(),tt(),T(),nt=E(z,[[`__scopeId`,`data-v-8492f1ff`]]),z.__docgenInfo=Object.assign({displayName:z.name??z.__name},{exportName:`default`,displayName:`CspSidebarLogo`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarLogo.vue`})})),B,it=e((()=>{i(),F(),B=c({__name:`CspSidebarProvider`,props:{defaultExpanded:{type:Boolean,default:!0},persistState:{type:Boolean,default:!0}},setup(e){let t=e;return xe({defaultExpanded:t.defaultExpanded,persistState:t.persistState}),(e,t)=>v(e.$slots,`default`)}})})),at,ot=e((()=>{it(),it(),at=B,B.__docgenInfo=Object.assign({displayName:B.name??B.__name},{exportName:`default`,displayName:`CspSidebarProvider`,type:1,props:[{name:`defaultExpanded`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`persistState`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`defaultExpanded`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`persistState`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarProvider.vue`})})),V,st=e((()=>{i(),ae(),F(),V=c({__name:`CspSidebarTrigger`,setup(e){let{toggle:t,isMobile:r}=P();return(e,i)=>l(r)?(b(),n(oe,{key:0,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:menu-line`,"aria-label":`Ouvrir le menu`,onClick:l(t)},null,8,[`onClick`])):f(``,!0)}})})),ct,lt=e((()=>{st(),st(),ct=V,V.__docgenInfo=Object.assign({displayName:V.name??V.__name},{exportName:`default`,displayName:`CspSidebarTrigger`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarTrigger.vue`})}));function ut(){return Math.random().toString(36).slice(2,11)}function dt(e){let{baseUrl:t=``,Request:n=globalThis.Request,fetch:r=globalThis.fetch,querySerializer:i,bodySerializer:a,pathSerializer:o,headers:s,requestInitExt:c=void 0,...l}={...e};c=xt()?c:void 0,t=yt(t);let u=[];async function d(e,d){let{baseUrl:f,fetch:p=r,Request:m=n,headers:h,params:g={},parseAs:_=`json`,querySerializer:v,bodySerializer:y=a??gt,pathSerializer:b,body:ee,middleware:x=[],...te}=d||{},S=t;f&&(S=yt(f)??t);let C=typeof i==`function`?i:mt(i);v&&(C=typeof v==`function`?v:mt({...typeof i==`object`?i:{},...v}));let ne=b||o||ht,w=ee===void 0?void 0:y(ee,vt(s,h,g.header)),T=vt(w===void 0||w instanceof FormData?{}:{"Content-Type":`application/json`},s,h,g.header),E=[...u,...x],D={redirect:`follow`,...l,...te,body:w,headers:T},O,k,A=new m(_t(e,{baseUrl:S,params:g,querySerializer:C,pathSerializer:ne}),D),j;for(let e in te)e in A||(A[e]=te[e]);if(E.length){O=ut(),k=Object.freeze({baseUrl:S,fetch:p,parseAs:_,querySerializer:C,bodySerializer:y,pathSerializer:ne});for(let t of E)if(t&&typeof t==`object`&&typeof t.onRequest==`function`){let n=await t.onRequest({request:A,schemaPath:e,params:g,options:k,id:O});if(n)if(n instanceof m)A=n;else if(n instanceof Response){j=n;break}else throw Error(`onRequest: must return new Request() or Response() when modifying the request`)}}if(!j){try{j=await p(A,c)}catch(t){let n=t;if(E.length)for(let t=E.length-1;t>=0;t--){let r=E[t];if(r&&typeof r==`object`&&typeof r.onError==`function`){let t=await r.onError({request:A,error:n,schemaPath:e,params:g,options:k,id:O});if(t){if(t instanceof Response){n=void 0,j=t;break}if(t instanceof Error){n=t;continue}throw Error(`onError: must return new Response() or instance of Error`)}}}if(n)throw n}if(E.length)for(let t=E.length-1;t>=0;t--){let n=E[t];if(n&&typeof n==`object`&&typeof n.onResponse==`function`){let t=await n.onResponse({request:A,response:j,schemaPath:e,params:g,options:k,id:O});if(t){if(!(t instanceof Response))throw Error(`onResponse: must return new Response() when modifying the response`);j=t}}}}let re=j.headers.get(`Content-Length`);if(j.status===204||A.method===`HEAD`||re===`0`&&!j.headers.get(`Transfer-Encoding`)?.includes(`chunked`))return j.ok?{data:void 0,response:j}:{error:void 0,response:j};if(j.ok)return{data:await(async()=>{if(_===`stream`)return j.body;if(_===`json`&&!re){let e=await j.text();return e?JSON.parse(e):void 0}return await j[_]()})(),response:j};let M=await j.text();try{M=JSON.parse(M)}catch{}return{error:M,response:j}}return{request(e,t,n){return d(t,{...n,method:e.toUpperCase()})},GET(e,t){return d(e,{...t,method:`GET`})},PUT(e,t){return d(e,{...t,method:`PUT`})},POST(e,t){return d(e,{...t,method:`POST`})},DELETE(e,t){return d(e,{...t,method:`DELETE`})},OPTIONS(e,t){return d(e,{...t,method:`OPTIONS`})},HEAD(e,t){return d(e,{...t,method:`HEAD`})},PATCH(e,t){return d(e,{...t,method:`PATCH`})},TRACE(e,t){return d(e,{...t,method:`TRACE`})},use(...e){for(let t of e)if(t){if(typeof t!=`object`||!(`onRequest`in t||`onResponse`in t||`onError`in t))throw Error("Middleware must be an object with one of `onRequest()`, `onResponse() or `onError()`");u.push(t)}},eject(...e){for(let t of e){let e=u.indexOf(t);e!==-1&&u.splice(e,1)}}}}function H(e,t,n){if(t==null)return``;if(typeof t==`object`)throw Error("Deeply-nested arrays/objects aren’t supported. Provide your own `querySerializer()` to handle these.");return`${e}=${n?.allowReserved===!0?t:encodeURIComponent(t)}`}function ft(e,t,n){if(!t||typeof t!=`object`)return``;let r=[],i={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`;if(n.style!==`deepObject`&&n.explode===!1){for(let e in t)r.push(e,n.allowReserved===!0?t[e]:encodeURIComponent(t[e]));let i=r.join(`,`);switch(n.style){case`form`:return`${e}=${i}`;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return i}}for(let i in t){let a=n.style===`deepObject`?`${e}[${i}]`:i;r.push(H(a,t[i],n))}let a=r.join(i);return n.style===`label`||n.style===`matrix`?`${i}${a}`:a}function pt(e,t,n){if(!Array.isArray(t))return``;if(n.explode===!1){let r={form:`,`,spaceDelimited:`%20`,pipeDelimited:`|`}[n.style]||`,`,i=(n.allowReserved===!0?t:t.map(e=>encodeURIComponent(e))).join(r);switch(n.style){case`simple`:return i;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return`${e}=${i}`}}let r={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`,i=[];for(let r of t)n.style===`simple`||n.style===`label`?i.push(n.allowReserved===!0?r:encodeURIComponent(r)):i.push(H(e,r,n));return n.style===`label`||n.style===`matrix`?`${r}${i.join(r)}`:i.join(r)}function mt(e){return function(t){let n=[];if(t&&typeof t==`object`)for(let r in t){let i=t[r];if(i!=null){if(Array.isArray(i)){if(i.length===0)continue;n.push(pt(r,i,{style:`form`,explode:!0,...e?.array,allowReserved:e?.allowReserved||!1}));continue}if(typeof i==`object`){n.push(ft(r,i,{style:`deepObject`,explode:!0,...e?.object,allowReserved:e?.allowReserved||!1}));continue}n.push(H(r,i,e))}}return n.join(`&`)}}function ht(e,t){let n=e;for(let r of e.match(bt)??[]){let e=r.substring(1,r.length-1),i=!1,a=`simple`;if(e.endsWith(`*`)&&(i=!0,e=e.substring(0,e.length-1)),e.startsWith(`.`)?(a=`label`,e=e.substring(1)):e.startsWith(`;`)&&(a=`matrix`,e=e.substring(1)),!t||t[e]===void 0||t[e]===null)continue;let o=t[e];if(Array.isArray(o)){n=n.replace(r,pt(e,o,{style:a,explode:i}));continue}if(typeof o==`object`){n=n.replace(r,ft(e,o,{style:a,explode:i}));continue}if(a===`matrix`){n=n.replace(r,`;${H(e,o)}`);continue}n=n.replace(r,a===`label`?`.${encodeURIComponent(o)}`:encodeURIComponent(o))}return n}function gt(e,t){return e instanceof FormData?e:t&&(t.get instanceof Function?t.get(`Content-Type`)??t.get(`content-type`):t[`Content-Type`]??t[`content-type`])===`application/x-www-form-urlencoded`?new URLSearchParams(e).toString():JSON.stringify(e)}function _t(e,t){let n=`${t.baseUrl}${e}`;t.params?.path&&(n=t.pathSerializer(n,t.params.path));let r=t.querySerializer(t.params.query??{});return r.startsWith(`?`)&&(r=r.substring(1)),r&&(n+=`?${r}`),n}function vt(...e){let t=new Headers;for(let n of e){if(!n||typeof n!=`object`)continue;let e=n instanceof Headers?n.entries():Object.entries(n);for(let[n,r]of e)if(r===null)t.delete(n);else if(Array.isArray(r))for(let e of r)t.append(n,e);else r!==void 0&&t.set(n,r)}return t}function yt(e){return e.endsWith(`/`)?e.substring(0,e.length-1):e}var bt,xt,St=e((()=>{bt=/\{[^{}]+\}/g,xt=()=>typeof process==`object`&&Number.parseInt(process?.versions?.node?.substring(0,2))>=18&&process.versions.undici}));function Ct(e){if(!e||typeof e!=`object`||Array.isArray(e))return{};let t=e,n=t.status===`error`&&t.details&&typeof t.details==`object`&&!Array.isArray(t.details)?t.details:t,r={};for(let[e,i]of Object.entries(n))if(!(n===t&&Et.has(e)))if(Array.isArray(i)){let t=i.filter(e=>typeof e==`string`);t.length>0&&(r[e]=t)}else typeof i==`string`&&(r[e]=[i]);return r}var U,wt,Tt,Et,Dt=e((()=>{U=class extends Error{status;statusText;data;constructor(e,t,n){super(`HTTP ${e}: ${t}`),this.status=e,this.statusText=t,this.data=n,this.name=`HttpError`}},wt=class extends Error{cause;constructor(e){super(`Network request failed`),this.cause=e,this.name=`NetworkError`}},Tt=class extends U{fieldErrors;constructor(e,t,n,r){super(e,t,n),this.fieldErrors=r,this.name=`ValidationError`}},Et=new Set([`detail`,`status`,`message`,`type`])}));function Ot(){let e=document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);return e?decodeURIComponent(e[1]):``}function kt(){let e=encodeURIComponent(window.location.pathname+window.location.search);throw window.location.href=`/utilisateur/connexion?next=${e}`,Error(`Redirecting to login`)}function At(e){let t=[`GET`,`POST`,`PUT`,`PATCH`,`DELETE`,`HEAD`,`OPTIONS`,`TRACE`],n={...e};for(let r of t){let t=e[r];n[r]=async(...e)=>{try{return await t(...e)}catch(e){throw e instanceof DOMException&&e.name===`AbortError`||e instanceof U||e instanceof Error&&e.message===`Redirecting to login`?e:new wt(e)}}}return n}var jt,Mt,W,Nt=e((()=>{St(),Dt(),jt={async onRequest({request:e}){if(e.method!==`GET`)return e.headers.set(`X-CSRFToken`,Ot()),e}},Mt={async onResponse({response:e}){if(e.ok)return;e.status===401&&kt();let t=await e.clone().json().catch(()=>void 0);throw e.status===400||e.status===422?new Tt(e.status,e.statusText,t,Ct(t)):new U(e.status,e.statusText,t)}},W=dt({baseUrl:typeof window<`u`?window.location.origin:``,credentials:`same-origin`,fetch:(...e)=>globalThis.fetch(...e)}),W.use(jt),W.use(Mt),At(W)}));async function Pt(){await fetch(`/utilisateur/deconnexion`,{method:`POST`,credentials:`same-origin`,headers:{"X-CSRFToken":Ot()}}),window.location.href=`/`}var Ft=e((()=>{Nt()}));function It(){return typeof window>`u`?!1:window.matchMedia(`(prefers-color-scheme: dark)`).matches}function G(e){typeof document>`u`||document.documentElement.setAttribute(`data-fr-theme`,e?`dark`:`light`)}function Lt(){let e=u(()=>K.value===`system`?q.value:K.value===`dark`);function t(t){K.value=t,localStorage.setItem(Rt,t),G(e.value)}function n(){t(e.value?`light`:`dark`)}let r=null,i=null;return x(()=>{q.value=It();let t=localStorage.getItem(Rt);t&&[`light`,`dark`,`system`].includes(t)&&(K.value=t),G(e.value),r=window.matchMedia(`(prefers-color-scheme: dark)`),i=e=>{q.value=e.matches,K.value===`system`&&G(e.matches)},r.addEventListener(`change`,i)}),_(()=>{r&&i&&r.removeEventListener(`change`,i)}),m(e,e=>{G(e)}),{colorMode:K,isDark:e,setColorMode:t,toggle:n}}var Rt,K,q,zt=e((()=>{i(),Rt=`csp_color_mode`,K=t(`system`),q=t(!1)})),Bt,Vt,Ht,J,Ut=e((()=>{i(),Ft(),ne(),se(),D(),zt(),F(),Bt={key:0,class:`csp-sidebar-user__info`},Vt={class:`csp-sidebar-user__name`},Ht={key:0,class:`csp-sidebar-user__role`},J=c({__name:`CspSidebarUser`,props:{name:{},role:{}},setup(e){let{isExpanded:t,isMobile:i}=P(),{isDark:s,toggle:c}=Lt();return(u,p)=>(b(),n(ce,{side:`right`,align:`end`,sections:[{items:[{label:l(s)?`Mode clair`:`Mode sombre`,icon:l(s)?`ri:sun-line`:`ri:moon-line`,onSelect:l(c)}]},{items:[{label:`Mon profil`,icon:`ri:user-line`},{label:`Paramètres`,icon:`ri:settings-3-line`}]},{items:[{label:`Se déconnecter`,icon:`ri:logout-box-r-line`,destructive:!0,onSelect:l(Pt)}]}]},{trigger:S(()=>[C(`button`,{type:`button`,class:r([`csp-sidebar-user`,{"csp-sidebar-user--expanded":l(t)||l(i)}])},[a(w,{name:e.name,size:`md`},null,8,[`name`]),l(t)||l(i)?(b(),o(`div`,Bt,[C(`span`,Vt,d(e.name),1),e.role?(b(),o(`span`,Ht,d(e.role),1)):f(``,!0)])):f(``,!0),l(t)||l(i)?(b(),n(O,{key:1,name:`ri:expand-up-down-line`,size:16,class:`csp-sidebar-user__chevron`})):f(``,!0)],2)]),_:1},8,[`sections`]))}})})),Wt=e((()=>{})),Gt,Kt=e((()=>{Ut(),Ut(),Wt(),T(),Gt=E(J,[[`__scopeId`,`data-v-eb144a6d`]]),J.__docgenInfo=Object.assign({displayName:J.name??J.__name},{exportName:`default`,displayName:`CspSidebarUser`,type:1,props:[{name:`name`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`role`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`name`,type:`string`,description:``,declarations:[],schema:`string`},{name:`role`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarUser.vue`})})),qt,Jt,Y,X,Z,Q,$,Yt;e((()=>{g(),ye(),ze(),Ke(),Ze(),rt(),ot(),lt(),Kt(),qt={title:`Compositions/Génériques/CspSidebar`,component:at,parameters:{layout:`fullscreen`,docs:{description:{component:`
Sidebar de navigation adaptée au DSFR.

## Composants

- \`CspSidebarProvider\` : contexte partagé (état, mobile, raccourcis)
- \`CspSidebar\` : panneau de navigation
- \`CspSidebarTrigger\` : bouton hamburger mobile (dans le header)
- \`CspSidebarGroup\`, \`CspSidebarItem\`, \`CspSidebarLogo\`, \`CspSidebarUser\`

## Usage

\`\`\`vue
<CspSidebarProvider default-expanded>
  <CspAppLayout>
    <template #sidebar>
      <CspSidebar>...</CspSidebar>
    </template>
    <template #header>
      <CspSidebarTrigger />
    </template>
    <!-- contenu -->
  </CspAppLayout>
</CspSidebarProvider>
\`\`\`
        `}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},Jt=`
  <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
    <CspAppLayout>
      <template #sidebar>
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
      </template>

      <template #header>
        <CspSidebarTrigger />
      </template>

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
    </CspAppLayout>
  </CspSidebarProvider>
`,Y={CspAppLayout:ve,CspSidebar:Re,CspSidebarGroup:Ge,CspSidebarItem:Xe,CspSidebarLogo:nt,CspSidebarProvider:at,CspSidebarTrigger:ct,CspSidebarUser:Gt},X={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:Jt})},Z={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:Jt})},Q={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:Jt})},$={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:Y,setup(){let t=y();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
      <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
        <CspAppLayout>
          <template #sidebar>
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
          </template>

          <template #header>
            <CspSidebarTrigger />
          </template>

          <div style="padding: 2rem;">
            <p style="color: var(--text-mention-grey); margin: 0;">
              Cliquez une entrée pour naviguer. Route active :
              <code style="padding: 0.125rem 0.375rem; border-radius: 0.25rem; background: var(--background-contrast-grey); font-family: monospace;">{{ route.path }}</code>
            </p>
          </div>
        </CspAppLayout>
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
        <CspAppLayout>
          <template #sidebar>
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
          </template>

          <template #header>
            <CspSidebarTrigger />
          </template>

          <div style="padding: 2rem;">
            <p style="color: var(--text-mention-grey); margin: 0;">
              Cliquez une entrée pour naviguer. Route active :
              <code style="padding: 0.125rem 0.375rem; border-radius: 0.25rem; background: var(--background-contrast-grey); font-family: monospace;">{{ route.path }}</code>
            </p>
          </div>
        </CspAppLayout>
      </CspSidebarProvider>
    \`
  })
}`,...$.parameters?.docs?.source}}},Yt=[`Default`,`Collapsed`,`Mobile`,`WithRouterLinks`]}))();export{Z as Collapsed,X as Default,Q as Mobile,$ as WithRouterLinks,Yt as __namedExportsOrder,qt as default};