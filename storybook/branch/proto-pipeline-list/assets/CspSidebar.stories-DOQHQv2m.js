import{i as e}from"./preload-helper-QkcEG8nj.js";import{B as t,D as n,Gt as r,H as i,Ht as a,K as o,Q as s,U as c,V as l,Wt as u,_t as d,at as f,bt as p,ct as ee,gt as m,i as h,it as g,jt as _,o as te,q as v,r as ne,st as y,ut as b,z as x,zt as S}from"./iframe-ByzLeagf.js";import{n as re,t as ie}from"./CspAvatar-gvh4R_Kw.js";import{n as C,t as w}from"./_plugin-vue_export-helper-Cx75YzON.js";import{En as ae,bn as oe,gn as se,mn as ce,t as le,wn as ue}from"./dist-CTKFvn_0.js";import{n as T,t as E}from"./CspIcon-HxkeVBB3.js";import{n as de,t as fe}from"./CspButton-8u3AJ3l5.js";import{n as pe,t as me}from"./CspDropdownMenu-CeEKu20o.js";import{n as he,t as ge}from"./CspTooltip-CXR1p1Hl.js";var _e,ve,ye,be,xe,D,Se=e((()=>{n(),_e={class:`csp-app-layout`},ve={class:`csp-app-layout__sidebar`},ye={class:`csp-app-layout__content`},be={key:0,class:`csp-app-layout__header`},xe={class:`csp-app-layout__main`},D=v({__name:`CspAppLayout`,setup(e){let n=m(),r=x(()=>!!n.header);return(e,n)=>(y(),c(`div`,_e,[t(`aside`,ve,[b(e.$slots,`sidebar`,{},void 0,!0)]),t(`div`,ye,[r.value?(y(),c(`header`,be,[b(e.$slots,`header`,{},void 0,!0)])):i(``,!0),t(`main`,xe,[b(e.$slots,`default`,{},void 0,!0)])])]))}})})),Ce=e((()=>{})),we,Te=e((()=>{Se(),Se(),Ce(),C(),we=w(D,[[`__scopeId`,`data-v-8ce26768`]]),D.__docgenInfo=Object.assign({displayName:D.name??D.__name},{exportName:`default`,displayName:`CspAppLayout`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`sidebar`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`header`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspAppLayout/CspAppLayout.vue`})}));function Ee(e){let t=_(!1);function n(){typeof window<`u`&&(t.value=window.innerWidth<=e)}return g(()=>{n(),window.addEventListener(`resize`,n)}),f(()=>{window.removeEventListener(`resize`,n)}),t}function O(e){let{defaultExpanded:t=!0,persistState:n=!0}=e,r=localStorage.getItem(A),i=_(r===null?t:r===`true`),a=Ee(768),o=_(!1),s=x(()=>i.value?`expanded`:`collapsed`);function c(e){i.value=e,n&&localStorage.setItem(A,String(e))}function l(e){o.value=e}function u(){a.value?l(!o.value):c(!i.value)}function p(e){e.key===`b`&&(e.metaKey||e.ctrlKey)&&(e.preventDefault(),u())}g(()=>{window.addEventListener(`keydown`,p)}),f(()=>{window.removeEventListener(`keydown`,p)}),d(a,e=>{!e&&o.value&&(o.value=!1)});let m={state:s,isExpanded:i,isMobile:a,isMobileOpen:o,setExpanded:c,setMobileOpen:l,toggle:u};return ee(M,m),m}function k(){let e=s(M);if(!e)throw Error(`useSidebar must be used within a CspSidebar provider`);return e}var A,j,De,M,N=e((()=>{n(),A=`csp_sidebar_state`,j=`15rem`,De=`4rem`,M=Symbol(`sidebar`),O.__docgenInfo=Object.assign({displayName:O.name??O.__name},{exportName:`provideSidebar`,displayName:`provideSidebar`,type:2,props:[{name:`defaultExpanded`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`persistState`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/composables/useSidebar.ts`})})),Oe,ke,Ae,je,Me,Ne,Pe,Fe,Ie,Le,P,Re=e((()=>{n(),le(),de(),T(),N(),Oe={class:`csp-sidebar__header`},ke={key:0,class:`csp-sidebar__brand`},Ae={class:`csp-sidebar__nav`},je={key:0,class:`csp-sidebar__footer`},Me=[`data-state`,`aria-expanded`],Ne={class:`csp-sidebar__header`},Pe={key:0,class:`csp-sidebar__brand`},Fe=[`aria-label`,`title`],Ie={class:`csp-sidebar__nav`},Le={key:0,class:`csp-sidebar__footer`},P=v({__name:`CspSidebar`,setup(e){let n=m(),r=x(()=>!!n.logo),s=x(()=>!!n.footer),{state:d,isExpanded:f,isMobile:ee,isMobileOpen:h,setMobileOpen:g,toggle:_}=k();return(e,n)=>S(ee)?(y(),l(S(ue),{key:0,open:S(h),"onUpdate:open":S(g)},{default:p(()=>[o(S(ce),null,{default:p(()=>[o(S(se),{class:`csp-sidebar-overlay`}),o(S(oe),{class:`csp-sidebar csp-sidebar--mobile`,"aria-label":e.$attrs[`aria-label`]??`Menu de navigation`,style:u({"--sidebar-width":S(j)})},{default:p(()=>[t(`header`,Oe,[r.value?(y(),c(`div`,ke,[b(e.$slots,`logo`,{},void 0,!0)])):i(``,!0),o(fe,{class:`csp-sidebar__close`,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":`Fermer le menu`,onClick:n[0]||=e=>S(g)(!1)})]),t(`nav`,Ae,[b(e.$slots,`default`,{},void 0,!0)]),s.value?(y(),c(`div`,je,[b(e.$slots,`footer`,{},void 0,!0)])):i(``,!0)]),_:3},8,[`aria-label`,`style`])]),_:3})]),_:3},8,[`open`,`onUpdate:open`])):(y(),c(`nav`,{key:1,class:a([`csp-sidebar`,{"csp-sidebar--expanded":S(f)}]),"data-state":S(d),"aria-expanded":S(f),style:u({"--sidebar-width":S(j),"--sidebar-width-collapsed":S(De)})},[t(`div`,Ne,[r.value&&S(f)?(y(),c(`div`,Pe,[b(e.$slots,`logo`,{},void 0,!0)])):i(``,!0),t(`button`,{type:`button`,class:`csp-sidebar__toggle`,"aria-label":S(f)?`Réduire le menu`:`Ouvrir le menu`,title:`${S(f)?`Réduire`:`Ouvrir`} (Ctrl+B)`,onClick:n[1]||=(...e)=>S(_)&&S(_)(...e)},[o(E,{name:S(f)?`ri:sidebar-fold-line`:`ri:sidebar-unfold-line`,size:18},null,8,[`name`])],8,Fe)]),t(`div`,Ie,[b(e.$slots,`default`,{},void 0,!0)]),s.value?(y(),c(`div`,Le,[b(e.$slots,`footer`,{},void 0,!0)])):i(``,!0)],14,Me))}})})),ze=e((()=>{})),Be,Ve=e((()=>{Re(),Re(),ze(),C(),Be=w(P,[[`__scopeId`,`data-v-5ffd2063`]]),P.__docgenInfo=Object.assign({displayName:P.name??P.__name},{exportName:`default`,displayName:`CspSidebar`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`logo`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`footer`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebar.vue`})})),He,F,Ue,I,We=e((()=>{n(),N(),He=[`aria-label`],F={key:0,class:`csp-sidebar-group__label`},Ue={class:`csp-sidebar-group__items`},I=v({__name:`CspSidebarGroup`,props:{label:{}},setup(e){let{isExpanded:n,isMobile:a}=k();return(o,s)=>(y(),c(`div`,{class:`csp-sidebar-group`,role:`group`,"aria-label":e.label},[S(n)||S(a)?(y(),c(`span`,F,r(e.label),1)):i(``,!0),t(`div`,Ue,[b(o.$slots,`default`,{},void 0,!0)])],8,He))}})})),Ge=e((()=>{})),Ke,qe=e((()=>{We(),We(),Ge(),C(),Ke=w(I,[[`__scopeId`,`data-v-68698bfb`]]),I.__docgenInfo=Object.assign({displayName:I.name??I.__name},{exportName:`default`,displayName:`CspSidebarGroup`,type:1,props:[{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`label`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarGroup.vue`})})),Je,L,Ye=e((()=>{n(),le(),h(),T(),he(),N(),Je={key:0,class:`csp-sidebar-item__label`},L=v({__name:`CspSidebarItem`,props:{icon:{},label:{},to:{},isActive:{type:Boolean,default:!1}},setup(e){let{isExpanded:t,isMobile:n}=k();return(s,u)=>(y(),l(ge,{content:e.label,disabled:S(t)||S(n),side:`right`,"side-offset":12},{default:p(()=>[o(S(ae),{as:e.to?S(ne):`button`,to:e.to,type:e.to?void 0:`button`,class:a([`csp-sidebar-item`,{"csp-sidebar-item--active":e.isActive,"csp-sidebar-item--expanded":S(t)||S(n)}]),"aria-current":e.isActive?`page`:void 0},{default:p(()=>[o(E,{class:`csp-sidebar-item__icon`,name:e.icon,size:16},null,8,[`name`]),S(t)||S(n)?(y(),c(`span`,Je,r(e.label),1)):i(``,!0)]),_:1},8,[`as`,`to`,`type`,`class`,`aria-current`])]),_:1},8,[`content`,`disabled`]))}})})),Xe=e((()=>{})),Ze,Qe=e((()=>{Ye(),Ye(),Xe(),C(),Ze=w(L,[[`__scopeId`,`data-v-c0db44da`]]),L.__docgenInfo=Object.assign({displayName:L.name??L.__name},{exportName:`default`,displayName:`CspSidebarItem`,type:1,props:[{name:`icon`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`to`,global:!1,description:``,tags:[],required:!1,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,declarations:[],schema:{kind:`enum`,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,schema:[`string`,{kind:`object`,type:`RouteLocationAsRelativeGeneric`},{kind:`object`,type:`RouteLocationAsPathGeneric`}]}},{name:`isActive`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`isActive`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`icon`,type:`string`,description:``,declarations:[],schema:`string`},{name:`to`,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,description:``,declarations:[],schema:{kind:`enum`,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,schema:[`string`,{kind:`object`,type:`RouteLocationAsRelativeGeneric`},{kind:`object`,type:`RouteLocationAsPathGeneric`}]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarItem.vue`})})),$e,et,R,tt=e((()=>{n(),N(),$e={class:`csp-sidebar-logo`},et={key:0,class:`csp-sidebar-logo__subtitle`},R=v({__name:`CspSidebarLogo`,setup(e){let{isExpanded:n,isMobile:r}=k();return(e,a)=>(y(),c(`div`,$e,[a[0]||=t(`span`,{class:`csp-sidebar-logo__title`},`CSPLab`,-1),S(n)||S(r)?(y(),c(`span`,et,` ATS `)):i(``,!0)]))}})})),nt=e((()=>{})),rt,it=e((()=>{tt(),tt(),nt(),C(),rt=w(R,[[`__scopeId`,`data-v-a437d6e4`]]),R.__docgenInfo=Object.assign({displayName:R.name??R.__name},{exportName:`default`,displayName:`CspSidebarLogo`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarLogo.vue`})})),z,at=e((()=>{n(),N(),z=v({__name:`CspSidebarProvider`,props:{defaultExpanded:{type:Boolean,default:!0},persistState:{type:Boolean,default:!0}},setup(e){let t=e;return O({defaultExpanded:t.defaultExpanded,persistState:t.persistState}),(e,t)=>b(e.$slots,`default`)}})})),B,ot=e((()=>{at(),at(),B=z,z.__docgenInfo=Object.assign({displayName:z.name??z.__name},{exportName:`default`,displayName:`CspSidebarProvider`,type:1,props:[{name:`defaultExpanded`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`persistState`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`defaultExpanded`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`persistState`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarProvider.vue`})})),V,st=e((()=>{n(),de(),N(),V=v({__name:`CspSidebarTrigger`,setup(e){let{toggle:t,isMobile:n}=k();return(e,r)=>S(n)?(y(),l(fe,{key:0,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:menu-line`,"aria-label":`Ouvrir le menu`,onClick:S(t)},null,8,[`onClick`])):i(``,!0)}})})),ct,lt=e((()=>{st(),st(),ct=V,V.__docgenInfo=Object.assign({displayName:V.name??V.__name},{exportName:`default`,displayName:`CspSidebarTrigger`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarTrigger.vue`})}));function ut(){return typeof window>`u`?!1:window.matchMedia(`(prefers-color-scheme: dark)`).matches}function H(e){typeof document>`u`||document.documentElement.setAttribute(`data-fr-theme`,e?`dark`:`light`)}function dt(){let e=x(()=>W.value===`system`?G.value:W.value===`dark`);function t(t){W.value=t,localStorage.setItem(U,t),H(e.value)}function n(){t(e.value?`light`:`dark`)}let r=null,i=null;return g(()=>{G.value=ut();let t=localStorage.getItem(U);t&&[`light`,`dark`,`system`].includes(t)&&(W.value=t),H(e.value),r=window.matchMedia(`(prefers-color-scheme: dark)`),i=e=>{G.value=e.matches,W.value===`system`&&H(e.matches)},r.addEventListener(`change`,i)}),f(()=>{r&&i&&r.removeEventListener(`change`,i)}),d(e,e=>{H(e)}),{colorMode:W,isDark:e,setColorMode:t,toggle:n}}var U,W,G,ft=e((()=>{n(),U=`csp_color_mode`,W=_(`system`),G=_(!1)})),pt,mt,ht,K,gt=e((()=>{n(),re(),pe(),T(),ft(),N(),pt={key:0,class:`csp-sidebar-user__info`},mt={class:`csp-sidebar-user__name`},ht={key:0,class:`csp-sidebar-user__role`},K=v({__name:`CspSidebarUser`,props:{name:{},role:{}},setup(e){let{isExpanded:n,isMobile:s}=k(),{isDark:u,toggle:d}=dt();return(f,ee)=>(y(),l(me,{side:`right`,align:`end`,sections:[{items:[{label:S(u)?`Mode clair`:`Mode sombre`,icon:S(u)?`ri:sun-line`:`ri:moon-line`,onSelect:S(d)}]},{items:[{label:`Mon profil`,icon:`ri:user-line`},{label:`Paramètres`,icon:`ri:settings-3-line`}]},{items:[{label:`Se déconnecter`,icon:`ri:logout-box-r-line`,destructive:!0}]}]},{trigger:p(()=>[t(`button`,{type:`button`,class:a([`csp-sidebar-user`,{"csp-sidebar-user--expanded":S(n)||S(s)}])},[o(ie,{name:e.name,size:`md`},null,8,[`name`]),S(n)||S(s)?(y(),c(`div`,pt,[t(`span`,mt,r(e.name),1),e.role?(y(),c(`span`,ht,r(e.role),1)):i(``,!0)])):i(``,!0),S(n)||S(s)?(y(),l(E,{key:1,name:`ri:expand-up-down-line`,size:16,class:`csp-sidebar-user__chevron`})):i(``,!0)],2)]),_:1},8,[`sections`]))}})})),_t=e((()=>{})),vt,yt=e((()=>{gt(),gt(),_t(),C(),vt=w(K,[[`__scopeId`,`data-v-c65edb09`]]),K.__docgenInfo=Object.assign({displayName:K.name??K.__name},{exportName:`default`,displayName:`CspSidebarUser`,type:1,props:[{name:`name`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`role`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`name`,type:`string`,description:``,declarations:[],schema:`string`},{name:`role`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarUser.vue`})})),bt,q,J,Y,X,Z,Q,$;e((()=>{h(),Te(),Ve(),qe(),Qe(),it(),ot(),lt(),yt(),bt={title:`Compositions/Génériques/CspSidebar`,component:B,parameters:{layout:`fullscreen`,docs:{description:{component:`
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
        `}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},q=`
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
`,J={CspAppLayout:we,CspSidebar:Be,CspSidebarGroup:Ke,CspSidebarItem:Ze,CspSidebarLogo:rt,CspSidebarProvider:B,CspSidebarTrigger:ct,CspSidebarUser:vt},Y={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:J,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:q})},X={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:J,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:q})},Z={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:J,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:q})},Q={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:J,setup(){let t=te();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
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
    `})},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
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
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
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
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
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
}`,...Z.parameters?.docs?.source}}},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
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
}`,...Q.parameters?.docs?.source}}},$=[`Default`,`Collapsed`,`Mobile`,`WithRouterLinks`]}))();export{X as Collapsed,Y as Default,Z as Mobile,Q as WithRouterLinks,$ as __namedExportsOrder,bt as default};