import{i as e}from"./preload-helper-Ct_ODC0V.js";import{At as t,B as n,Bt as r,D as i,G as a,H as o,Ht as s,K as c,Lt as l,R as u,Ut as d,V as f,Z as p,gt as m,ht as h,i as g,it as _,lt as v,o as y,ot as b,r as ee,rt as x,st as te,yt as S,z as C}from"./iframe-fe_o0PNB.js";import{n as ne,t as re}from"./CspAvatar-ZGZcAC5Z.js";import{n as w,t as T}from"./_plugin-vue_export-helper-DAS0NJne.js";import{En as ie,bn as ae,gn as oe,mn as se,t as ce,wn as le}from"./dist-kBQ8eT5a.js";import{n as E,t as D}from"./CspIcon-qlJwYyGc.js";import{n as ue,t as de}from"./CspButton-ZdC5HkWu.js";import{n as fe,t as pe}from"./CspDropdownMenu-Cp6RdcAa.js";import{n as me,t as he}from"./CspTooltip-enrexAGU.js";var ge,_e,ve,ye,be,O,xe=e((()=>{i(),ge={class:`csp-app-layout`},_e={class:`csp-app-layout__sidebar`},ve={class:`csp-app-layout__content`},ye={key:0,class:`csp-app-layout__header`},be={class:`csp-app-layout__main`},O=c({__name:`CspAppLayout`,setup(e){let t=h(),n=u(()=>!!t.header);return(e,t)=>(b(),o(`div`,ge,[C(`aside`,_e,[v(e.$slots,`sidebar`,{},void 0,!0)]),C(`div`,ve,[n.value?(b(),o(`header`,ye,[v(e.$slots,`header`,{},void 0,!0)])):f(``,!0),C(`main`,be,[v(e.$slots,`default`,{},void 0,!0)])])]))}})})),Se=e((()=>{})),Ce,we=e((()=>{xe(),xe(),Se(),w(),Ce=T(O,[[`__scopeId`,`data-v-8ce26768`]]),O.__docgenInfo=Object.assign({displayName:O.name??O.__name},{exportName:`default`,displayName:`CspAppLayout`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`sidebar`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`header`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspAppLayout/CspAppLayout.vue`})}));function Te(e){let n=t(!1);function r(){typeof window<`u`&&(n.value=window.innerWidth<=e)}return x(()=>{r(),window.addEventListener(`resize`,r)}),_(()=>{window.removeEventListener(`resize`,r)}),n}function k(e){let{defaultExpanded:n=!0,persistState:r=!0}=e,i=localStorage.getItem(j),a=t(i===null?n:i===`true`),o=Te(768),s=t(!1),c=u(()=>a.value?`expanded`:`collapsed`);function l(e){a.value=e,r&&localStorage.setItem(j,String(e))}function d(e){s.value=e}function f(){o.value?d(!s.value):l(!a.value)}function p(e){e.key===`b`&&(e.metaKey||e.ctrlKey)&&(e.preventDefault(),f())}x(()=>{window.addEventListener(`keydown`,p)}),_(()=>{window.removeEventListener(`keydown`,p)}),m(o,e=>{!e&&s.value&&(s.value=!1)});let h={state:c,isExpanded:a,isMobile:o,isMobileOpen:s,setExpanded:l,setMobileOpen:d,toggle:f};return te(N,h),h}function A(){let e=p(N);if(!e)throw Error(`useSidebar must be used within a CspSidebar provider`);return e}var j,M,Ee,N,P=e((()=>{i(),j=`csp_sidebar_state`,M=`15rem`,Ee=`4rem`,N=Symbol(`sidebar`),k.__docgenInfo=Object.assign({displayName:k.name??k.__name},{exportName:`provideSidebar`,displayName:`provideSidebar`,type:2,props:[{name:`defaultExpanded`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`persistState`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/composables/useSidebar.ts`})})),De,Oe,ke,Ae,je,Me,Ne,Pe,Fe,Ie,F,Le=e((()=>{i(),ce(),ue(),E(),P(),De={class:`csp-sidebar__header`},Oe={key:0,class:`csp-sidebar__brand`},ke={class:`csp-sidebar__nav`},Ae={key:0,class:`csp-sidebar__footer`},je=[`data-state`,`aria-expanded`],Me={class:`csp-sidebar__header`},Ne={key:0,class:`csp-sidebar__brand`},Pe=[`aria-label`,`title`],Fe={class:`csp-sidebar__nav`},Ie={key:0,class:`csp-sidebar__footer`},F=c({__name:`CspSidebar`,setup(e){let t=h(),i=u(()=>!!t.logo),c=u(()=>!!t.footer),{state:d,isExpanded:p,isMobile:m,isMobileOpen:g,setMobileOpen:_,toggle:y}=A();return(e,t)=>l(m)?(b(),n(l(le),{key:0,open:l(g),"onUpdate:open":l(_)},{default:S(()=>[a(l(se),null,{default:S(()=>[a(l(oe),{class:`csp-sidebar-overlay`}),a(l(ae),{class:`csp-sidebar csp-sidebar--mobile`,"aria-label":e.$attrs[`aria-label`]??`Menu de navigation`,style:s({"--sidebar-width":l(M)})},{default:S(()=>[C(`header`,De,[i.value?(b(),o(`div`,Oe,[v(e.$slots,`logo`,{},void 0,!0)])):f(``,!0),a(de,{class:`csp-sidebar__close`,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":`Fermer le menu`,onClick:t[0]||=e=>l(_)(!1)})]),C(`nav`,ke,[v(e.$slots,`default`,{},void 0,!0)]),c.value?(b(),o(`div`,Ae,[v(e.$slots,`footer`,{},void 0,!0)])):f(``,!0)]),_:3},8,[`aria-label`,`style`])]),_:3})]),_:3},8,[`open`,`onUpdate:open`])):(b(),o(`nav`,{key:1,class:r([`csp-sidebar`,{"csp-sidebar--expanded":l(p)}]),"data-state":l(d),"aria-expanded":l(p),style:s({"--sidebar-width":l(M),"--sidebar-width-collapsed":l(Ee)})},[C(`div`,Me,[i.value&&l(p)?(b(),o(`div`,Ne,[v(e.$slots,`logo`,{},void 0,!0)])):f(``,!0),C(`button`,{type:`button`,class:`csp-sidebar__toggle`,"aria-label":l(p)?`Réduire le menu`:`Ouvrir le menu`,title:`${l(p)?`Réduire`:`Ouvrir`} (Ctrl+B)`,onClick:t[1]||=(...e)=>l(y)&&l(y)(...e)},[a(D,{name:l(p)?`ri:sidebar-fold-line`:`ri:sidebar-unfold-line`,size:18},null,8,[`name`])],8,Pe)]),C(`div`,Fe,[v(e.$slots,`default`,{},void 0,!0)]),c.value?(b(),o(`div`,Ie,[v(e.$slots,`footer`,{},void 0,!0)])):f(``,!0)],14,je))}})})),Re=e((()=>{})),ze,Be=e((()=>{Le(),Le(),Re(),w(),ze=T(F,[[`__scopeId`,`data-v-5ffd2063`]]),F.__docgenInfo=Object.assign({displayName:F.name??F.__name},{exportName:`default`,displayName:`CspSidebar`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`logo`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`footer`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebar.vue`})})),Ve,I,He,L,Ue=e((()=>{i(),P(),Ve=[`aria-label`],I={key:0,class:`csp-sidebar-group__label`},He={class:`csp-sidebar-group__items`},L=c({__name:`CspSidebarGroup`,props:{label:{}},setup(e){let{isExpanded:t,isMobile:n}=A();return(r,i)=>(b(),o(`div`,{class:`csp-sidebar-group`,role:`group`,"aria-label":e.label},[l(t)||l(n)?(b(),o(`span`,I,d(e.label),1)):f(``,!0),C(`div`,He,[v(r.$slots,`default`,{},void 0,!0)])],8,Ve))}})})),We=e((()=>{})),Ge,Ke=e((()=>{Ue(),Ue(),We(),w(),Ge=T(L,[[`__scopeId`,`data-v-68698bfb`]]),L.__docgenInfo=Object.assign({displayName:L.name??L.__name},{exportName:`default`,displayName:`CspSidebarGroup`,type:1,props:[{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`label`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarGroup.vue`})})),qe,R,Je=e((()=>{i(),ce(),g(),E(),me(),P(),qe={key:0,class:`csp-sidebar-item__label`},R=c({inheritAttrs:!1,__name:`CspSidebarItem`,props:{icon:{},label:{},to:{},isActive:{type:Boolean,default:!1}},setup(e){let{isExpanded:t,isMobile:i}=A();return(s,c)=>(b(),n(he,{content:e.label,disabled:l(t)||l(i),side:`right`,"side-offset":12},{default:S(()=>[a(l(ie),{as:e.to?l(ee):`button`,to:e.to,type:e.to?void 0:`button`,class:r([`csp-sidebar-item`,{"csp-sidebar-item--active":e.isActive,"csp-sidebar-item--expanded":l(t)||l(i)}]),"aria-current":e.isActive?`page`:void 0},{default:S(()=>[a(D,{class:`csp-sidebar-item__icon`,name:e.icon,size:16},null,8,[`name`]),l(t)||l(i)?(b(),o(`span`,qe,d(e.label),1)):f(``,!0)]),_:1},8,[`as`,`to`,`type`,`class`,`aria-current`])]),_:1},8,[`content`,`disabled`]))}})})),Ye=e((()=>{})),Xe,Ze=e((()=>{Je(),Je(),Ye(),w(),Xe=T(R,[[`__scopeId`,`data-v-9ebe728d`]]),R.__docgenInfo=Object.assign({displayName:R.name??R.__name},{exportName:`default`,displayName:`CspSidebarItem`,type:1,props:[{name:`icon`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`to`,global:!1,description:``,tags:[],required:!1,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,declarations:[],schema:{kind:`enum`,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,schema:[`string`,{kind:`object`,type:`RouteLocationAsRelativeGeneric`},{kind:`object`,type:`RouteLocationAsPathGeneric`}]}},{name:`isActive`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`isActive`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`icon`,type:`string`,description:``,declarations:[],schema:`string`},{name:`to`,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,description:``,declarations:[],schema:{kind:`enum`,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,schema:[`string`,{kind:`object`,type:`RouteLocationAsRelativeGeneric`},{kind:`object`,type:`RouteLocationAsPathGeneric`}]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarItem.vue`})})),Qe,$e,z,et=e((()=>{i(),P(),Qe={class:`csp-sidebar-logo`},$e={key:0,class:`csp-sidebar-logo__subtitle`},z=c({__name:`CspSidebarLogo`,setup(e){let{isExpanded:t,isMobile:n}=A();return(e,r)=>(b(),o(`div`,Qe,[r[0]||=C(`span`,{class:`csp-sidebar-logo__title`},`CSPLab`,-1),l(t)||l(n)?(b(),o(`span`,$e,` ATS `)):f(``,!0)]))}})})),tt=e((()=>{})),nt,rt=e((()=>{et(),et(),tt(),w(),nt=T(z,[[`__scopeId`,`data-v-a437d6e4`]]),z.__docgenInfo=Object.assign({displayName:z.name??z.__name},{exportName:`default`,displayName:`CspSidebarLogo`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarLogo.vue`})})),B,it=e((()=>{i(),P(),B=c({__name:`CspSidebarProvider`,props:{defaultExpanded:{type:Boolean,default:!0},persistState:{type:Boolean,default:!0}},setup(e){let t=e;return k({defaultExpanded:t.defaultExpanded,persistState:t.persistState}),(e,t)=>v(e.$slots,`default`)}})})),V,at=e((()=>{it(),it(),V=B,B.__docgenInfo=Object.assign({displayName:B.name??B.__name},{exportName:`default`,displayName:`CspSidebarProvider`,type:1,props:[{name:`defaultExpanded`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`persistState`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`defaultExpanded`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`persistState`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarProvider.vue`})})),H,ot=e((()=>{i(),ue(),P(),H=c({__name:`CspSidebarTrigger`,setup(e){let{toggle:t,isMobile:r}=A();return(e,i)=>l(r)?(b(),n(de,{key:0,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:menu-line`,"aria-label":`Ouvrir le menu`,onClick:l(t)},null,8,[`onClick`])):f(``,!0)}})})),st,ct=e((()=>{ot(),ot(),st=H,H.__docgenInfo=Object.assign({displayName:H.name??H.__name},{exportName:`default`,displayName:`CspSidebarTrigger`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarTrigger.vue`})}));function lt(){return typeof window>`u`?!1:window.matchMedia(`(prefers-color-scheme: dark)`).matches}function U(e){typeof document>`u`||document.documentElement.setAttribute(`data-fr-theme`,e?`dark`:`light`)}function ut(){let e=u(()=>G.value===`system`?K.value:G.value===`dark`);function t(t){G.value=t,localStorage.setItem(W,t),U(e.value)}function n(){t(e.value?`light`:`dark`)}let r=null,i=null;return x(()=>{K.value=lt();let t=localStorage.getItem(W);t&&[`light`,`dark`,`system`].includes(t)&&(G.value=t),U(e.value),r=window.matchMedia(`(prefers-color-scheme: dark)`),i=e=>{K.value=e.matches,G.value===`system`&&U(e.matches)},r.addEventListener(`change`,i)}),_(()=>{r&&i&&r.removeEventListener(`change`,i)}),m(e,e=>{U(e)}),{colorMode:G,isDark:e,setColorMode:t,toggle:n}}var W,G,K,dt=e((()=>{i(),W=`csp_color_mode`,G=t(`system`),K=t(!1)})),ft,pt,mt,q,ht=e((()=>{i(),ne(),fe(),E(),dt(),P(),ft={key:0,class:`csp-sidebar-user__info`},pt={class:`csp-sidebar-user__name`},mt={key:0,class:`csp-sidebar-user__role`},q=c({__name:`CspSidebarUser`,props:{name:{},role:{}},setup(e){let{isExpanded:t,isMobile:i}=A(),{isDark:s,toggle:c}=ut();return(u,p)=>(b(),n(pe,{side:`right`,align:`end`,sections:[{items:[{label:l(s)?`Mode clair`:`Mode sombre`,icon:l(s)?`ri:sun-line`:`ri:moon-line`,onSelect:l(c)}]},{items:[{label:`Mon profil`,icon:`ri:user-line`},{label:`Paramètres`,icon:`ri:settings-3-line`}]},{items:[{label:`Se déconnecter`,icon:`ri:logout-box-r-line`,destructive:!0}]}]},{trigger:S(()=>[C(`button`,{type:`button`,class:r([`csp-sidebar-user`,{"csp-sidebar-user--expanded":l(t)||l(i)}])},[a(re,{name:e.name,size:`md`},null,8,[`name`]),l(t)||l(i)?(b(),o(`div`,ft,[C(`span`,pt,d(e.name),1),e.role?(b(),o(`span`,mt,d(e.role),1)):f(``,!0)])):f(``,!0),l(t)||l(i)?(b(),n(D,{key:1,name:`ri:expand-up-down-line`,size:16,class:`csp-sidebar-user__chevron`})):f(``,!0)],2)]),_:1},8,[`sections`]))}})})),gt=e((()=>{})),_t,vt=e((()=>{ht(),ht(),gt(),w(),_t=T(q,[[`__scopeId`,`data-v-c65edb09`]]),q.__docgenInfo=Object.assign({displayName:q.name??q.__name},{exportName:`default`,displayName:`CspSidebarUser`,type:1,props:[{name:`name`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`role`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`name`,type:`string`,description:``,declarations:[],schema:`string`},{name:`role`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspSidebar/CspSidebarUser.vue`})})),yt,J,Y,X,Z,Q,$,bt;e((()=>{g(),we(),Be(),Ke(),Ze(),rt(),at(),ct(),vt(),yt={title:`Compositions/Génériques/CspSidebar`,component:V,parameters:{layout:`fullscreen`,docs:{description:{component:`
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
        `}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},J=`
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
`,Y={CspAppLayout:Ce,CspSidebar:ze,CspSidebarGroup:Ge,CspSidebarItem:Xe,CspSidebarLogo:nt,CspSidebarProvider:V,CspSidebarTrigger:st,CspSidebarUser:_t},X={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Z={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},Q={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:Y,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:J})},$={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:Y,setup(){let t=y();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
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
}`,...$.parameters?.docs?.source}}},bt=[`Default`,`Collapsed`,`Mobile`,`WithRouterLinks`]}))();export{Z as Collapsed,X as Default,Q as Mobile,$ as WithRouterLinks,bt as __namedExportsOrder,yt as default};