import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,A as n,B as r,C as i,D as a,Dt as o,Et as s,G as c,H as l,I as u,N as d,O as f,Ot as p,Q as m,S as h,St as g,Tt as _,U as v,_ as ee,a as te,b as y,c as b,ht as x,i as ne,rt as S,s as re,w as C,x as w,z as T}from"./iframe-DzvP5sZ1.js";import{n as E,t as D}from"./CspIcon-MCaeL-8V.js";import{n as O,t as k}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as A,t as ie}from"./CspAvatar-B0xBQRrk.js";import{n as ae,t as oe}from"./CspSelect-B_2lpJTM.js";import{n as se,t as ce}from"./Primitive-BIEOoJmT.js";import{n as le,t as ue}from"./CspDropdownMenu-o0wTxE7l.js";import{n as de,t as fe}from"./CspTooltip-CyUBxBzX.js";import{a as pe,c as me,i as he,n as ge,o as _e,r as ve,s as ye,t as be}from"./DialogPortal-BWiI02U0.js";import{n as xe,t as Se}from"./CspButton-DR6fJ3Qq.js";import{n as Ce,t as we}from"./CspPageHeader-B3WM_Jtx.js";import{n as Te,r as Ee}from"./breakpoints-B2j6PB-K.js";function De(e){let t=x(!1),n;function i(){t.value=n?.matches??!1}return T(()=>{n=window.matchMedia(e),i(),n.addEventListener(`change`,i)}),r(()=>{n?.removeEventListener(`change`,i)}),t}function Oe(){return(Oe=e((()=>{b()})))()}function ke(e){let{defaultExpanded:n=!0,persistState:i=!0}=e,a=localStorage.getItem(Ae),o=x(a===null?n:a===`true`),s=De(Te(`lg`)),c=x(!1),l=y(()=>o.value?`expanded`:`collapsed`),u=y(()=>o.value||s.value);function d(e){o.value=e,i&&localStorage.setItem(Ae,String(e))}function f(e){c.value=e}function p(){s.value?f(!c.value):d(!o.value)}function m(e){e.key===`b`&&(e.metaKey||e.ctrlKey)&&(e.preventDefault(),p())}T(()=>{window.addEventListener(`keydown`,m)}),r(()=>{window.removeEventListener(`keydown`,m)}),t(s,e=>{!e&&c.value&&(c.value=!1)});let h={state:l,isExpanded:o,isMobile:s,isMobileOpen:c,showLabels:u,setExpanded:d,setMobileOpen:f,toggle:p};return v(Ne,h),h}function j(){let e=d(Ne);if(!e)throw Error(`useSidebar must be used within a CspSidebar provider`);return e}var Ae,je,Me,Ne;function M(){return(M=e((()=>{b(),Ee(),Oe(),Ae=`csp_sidebar_state`,je=`16rem`,Me=`4rem`,Ne=Symbol(`sidebar`)})))()}var Pe,Fe,Ie,Le,Re,ze,Be,Ve,He,Ue,We,Ge,N;function Ke(){return(Ke=e((()=>{b(),_e(),he(),ge(),me(),xe(),E(),M(),Pe={class:`csp-sidebar__header`},Fe={key:0,class:`csp-sidebar__brand`},Ie={class:`csp-sidebar__context`},Le={class:`csp-sidebar__nav`},Re={key:0,class:`csp-sidebar__footer`},ze=[`data-state`,`aria-expanded`],Be={class:`csp-sidebar__header`},Ve={key:0,class:`csp-sidebar__brand`},He=[`aria-label`,`title`],Ue={class:`csp-sidebar__context`},We={class:`csp-sidebar__nav`},Ge={key:0,class:`csp-sidebar__footer`},N=f({__name:`CspSidebar`,setup(e){let t=m(),n=y(()=>!!t.logo),r=y(()=>!!t.footer),{state:s,isExpanded:u,isMobile:d,isMobileOpen:f,setMobileOpen:p,toggle:v}=j();return(e,t)=>g(d)?(l(),h(g(ye),{key:0,open:g(f),"onUpdate:open":g(p)},{default:S(()=>[a(g(be),null,{default:S(()=>[a(g(ve),{class:`csp-sidebar-overlay`}),a(g(pe),{class:`csp-sidebar csp-sidebar--mobile`,"aria-label":e.$attrs[`aria-label`]??`Menu de navigation`,style:o({"--sidebar-width":g(je)})},{default:S(()=>[w(`header`,Pe,[n.value?(l(),C(`div`,Fe,[c(e.$slots,`logo`,{},void 0,!0)])):i(``,!0),a(Se,{class:`csp-sidebar__close`,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":`Fermer le menu`,onClick:t[0]||=e=>g(p)(!1)})]),w(`div`,Ie,[c(e.$slots,`context`,{},void 0,!0)]),w(`nav`,Le,[c(e.$slots,`default`,{},void 0,!0)]),r.value?(l(),C(`div`,Re,[c(e.$slots,`footer`,{},void 0,!0)])):i(``,!0)]),_:3},8,[`aria-label`,`style`])]),_:3})]),_:3},8,[`open`,`onUpdate:open`])):(l(),C(`nav`,{key:1,class:_([`csp-sidebar`,{"csp-sidebar--expanded":g(u)}]),"data-state":g(s),"aria-expanded":g(u),style:o({"--sidebar-width":g(je),"--sidebar-width-collapsed":g(Me)})},[w(`div`,Be,[n.value&&g(u)?(l(),C(`div`,Ve,[c(e.$slots,`logo`,{},void 0,!0)])):i(``,!0),w(`button`,{type:`button`,class:`csp-sidebar__toggle`,"aria-label":g(u)?`Réduire le menu`:`Ouvrir le menu`,title:`${g(u)?`Réduire`:`Ouvrir`} (Ctrl+B)`,onClick:t[1]||=(...e)=>g(v)&&g(v)(...e)},[a(D,{name:g(u)?`ri:sidebar-fold-line`:`ri:sidebar-unfold-line`,size:18},null,8,[`name`])],8,He)]),w(`div`,Ue,[c(e.$slots,`context`,{},void 0,!0)]),w(`div`,We,[c(e.$slots,`default`,{},void 0,!0)]),r.value?(l(),C(`div`,Ge,[c(e.$slots,`footer`,{},void 0,!0)])):i(``,!0)],14,ze))}})})))()}var qe;function Je(){return(Je=e((()=>{Ke(),O(),qe=k(N,[[`__scopeId`,`data-v-0642d2cd`]]),N.__docgenInfo=Object.assign({displayName:N.name??N.__name},{exportName:`default`,displayName:`CspSidebar`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[{name:`logo`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`context`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`default`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`footer`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebar.vue`})})))()}function Ye(e,t){return l(),C(`div`,Xe,[w(`div`,Ze,[c(e.$slots,`default`,{},void 0,!0)])])}var P,Xe,Ze,Qe;function $e(){return($e=e((()=>{b(),O(),P={},Xe={class:`csp-sidebar-group`},Ze={class:`csp-sidebar-group__items`},Qe=k(P,[[`render`,Ye],[`__scopeId`,`data-v-99e3ccf5`]]),P.__docgenInfo=Object.assign({displayName:P.name??P.__name},{exportName:`default`,displayName:`CspSidebarGroup`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[{name:`default`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarGroup.vue`})})))()}var et,F;function tt(){return(tt=e((()=>{b(),se(),te(),E(),de(),M(),et={key:0,class:`csp-sidebar-item__label`},F=f({inheritAttrs:!1,__name:`CspSidebarItem`,props:{icon:{},label:{},to:{},isActive:{type:Boolean,default:!1}},setup(e){let{showLabels:t}=j();return(n,r)=>(l(),h(fe,{content:e.label,disabled:g(t),side:`right`,"side-offset":12},{default:S(()=>[a(g(ce),{as:e.to?g(ne):`button`,to:e.to,type:e.to?void 0:`button`,class:_([`csp-sidebar-item`,{"csp-sidebar-item--active":e.isActive,"csp-sidebar-item--expanded":g(t)}]),"aria-current":e.isActive?`page`:void 0},{default:S(()=>[a(D,{class:`csp-sidebar-item__icon`,name:e.icon,size:16},null,8,[`name`]),g(t)?(l(),C(`span`,et,p(e.label),1)):i(``,!0)]),_:1},8,[`as`,`to`,`type`,`class`,`aria-current`])]),_:1},8,[`content`,`disabled`]))}})})))()}var nt;function rt(){return(rt=e((()=>{tt(),O(),nt=k(F,[[`__scopeId`,`data-v-3af70773`]]),F.__docgenInfo=Object.assign({displayName:F.name??F.__name},{exportName:`default`,displayName:`CspSidebarItem`,type:1,props:[{name:`icon`,global:!1,description:``,tags:[],required:!0,type:`string`,schema:`string`,declarations:[]},{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,schema:`string`,declarations:[]},{name:`to`,global:!1,description:``,tags:[],required:!1,type:`string | it | et | undefined`,schema:{kind:`enum`,type:`string | it | et | undefined`,schema:[`undefined`,`string`,{kind:`object`,type:`it`},{kind:`object`,type:`et`}]},declarations:[]},{name:`isActive`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarItem.vue`})})))()}var it,at,I;function ot(){return(ot=e((()=>{b(),M(),it={class:`csp-sidebar-logo`},at={key:0,class:`csp-sidebar-logo__subtitle`},I=f({__name:`CspSidebarLogo`,setup(e){let{showLabels:t}=j();return(e,n)=>(l(),C(`div`,it,[n[0]||=w(`span`,{class:`csp-sidebar-logo__title`},`CSPLab`,-1),g(t)?(l(),C(`span`,at,` ATS `)):i(``,!0)]))}})})))()}var st;function ct(){return(ct=e((()=>{ot(),O(),st=k(I,[[`__scopeId`,`data-v-c7543cb8`]]),I.__docgenInfo=Object.assign({displayName:I.name??I.__name},{exportName:`default`,displayName:`CspSidebarLogo`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarLogo.vue`})})))()}var L;function lt(){return(lt=e((()=>{b(),M(),L=f({__name:`CspSidebarProvider`,props:{defaultExpanded:{type:Boolean,default:!0},persistState:{type:Boolean,default:!0}},setup(e){let t=e;return ke({defaultExpanded:t.defaultExpanded,persistState:t.persistState}),(e,t)=>c(e.$slots,`default`)}})})))()}var ut;function dt(){return(dt=e((()=>{lt(),ut=L,L.__docgenInfo=Object.assign({displayName:L.name??L.__name},{exportName:`default`,displayName:`CspSidebarProvider`,type:1,props:[{name:`defaultExpanded`,global:!1,default:`true`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`persistState`,global:!1,default:`true`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[{name:`default`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarProvider.vue`})})))()}var R;function ft(){return(ft=e((()=>{b(),xe(),M(),R=f({__name:`CspSidebarTrigger`,setup(e){let{toggle:t,isMobile:n}=j();return(e,r)=>g(n)?(l(),h(Se,{key:0,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:menu-line`,"aria-label":`Ouvrir le menu`,onClick:g(t)},null,8,[`onClick`])):i(``,!0)}})})))()}var pt;function mt(){return(mt=e((()=>{ft(),pt=R,R.__docgenInfo=Object.assign({displayName:R.name??R.__name},{exportName:`default`,displayName:`CspSidebarTrigger`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarTrigger.vue`})})))()}function ht(){return Math.random().toString(36).slice(2,11)}function gt(e){let{baseUrl:t=``,Request:n=globalThis.Request,fetch:r=globalThis.fetch,querySerializer:i,bodySerializer:a,pathSerializer:o,headers:s,requestInitExt:c=void 0,...l}={...e};c=Et()?c:void 0,t=wt(t);let u=[];async function d(e,d){let{baseUrl:f,fetch:p=r,Request:m=n,headers:h,params:g={},parseAs:_=`json`,querySerializer:v,bodySerializer:ee=a??xt,pathSerializer:te,body:y,middleware:b=[],...x}=d||{},ne=t;f&&(ne=wt(f)??t);let S=typeof i==`function`?i:yt(i);v&&(S=typeof v==`function`?v:yt({...typeof i==`object`?i:{},...v}));let re=te||o||bt,C=y===void 0?void 0:ee(y,Ct(s,h,g.header)),w=Ct(C===void 0||C instanceof FormData?{}:{"Content-Type":`application/json`},s,h,g.header),T=[...u,...b],E={redirect:`follow`,...l,...x,body:C,headers:w},D,O,k=new m(St(e,{baseUrl:ne,params:g,querySerializer:S,pathSerializer:re}),E),A;for(let e in x)e in k||(k[e]=x[e]);if(T.length){D=ht(),O=Object.freeze({baseUrl:ne,fetch:p,parseAs:_,querySerializer:S,bodySerializer:ee,pathSerializer:re});for(let t of T)if(t&&typeof t==`object`&&typeof t.onRequest==`function`){let n=await t.onRequest({request:k,schemaPath:e,params:g,options:O,id:D});if(n){if(n instanceof m)k=n;else if(n instanceof Response){A=n;break}else throw Error(`onRequest: must return new Request() or Response() when modifying the request`)}}}if(!A){try{A=await p(k,c)}catch(t){let n=t;if(T.length)for(let t=T.length-1;t>=0;t--){let r=T[t];if(r&&typeof r==`object`&&typeof r.onError==`function`){let t=await r.onError({request:k,error:n,schemaPath:e,params:g,options:O,id:D});if(t){if(t instanceof Response){n=void 0,A=t;break}if(t instanceof Error){n=t;continue}throw Error(`onError: must return new Response() or instance of Error`)}}}if(n)throw n}if(T.length)for(let t=T.length-1;t>=0;t--){let n=T[t];if(n&&typeof n==`object`&&typeof n.onResponse==`function`){let t=await n.onResponse({request:k,response:A,schemaPath:e,params:g,options:O,id:D});if(t){if(!(t instanceof Response))throw Error(`onResponse: must return new Response() when modifying the response`);A=t}}}}let ie=A.headers.get(`Content-Length`);if(A.status===204||k.method===`HEAD`||ie===`0`&&!A.headers.get(`Transfer-Encoding`)?.includes(`chunked`))return A.ok?{data:void 0,response:A}:{error:void 0,response:A};if(A.ok)return{data:await(async()=>{if(_===`stream`)return A.body;if(_===`json`&&!ie){let e=await A.text();return e?JSON.parse(e):void 0}return await A[_]()})(),response:A};let ae=await A.text();try{ae=JSON.parse(ae)}catch{}return{error:ae,response:A}}return{request(e,t,n){return d(t,{...n,method:e.toUpperCase()})},GET(e,t){return d(e,{...t,method:`GET`})},PUT(e,t){return d(e,{...t,method:`PUT`})},POST(e,t){return d(e,{...t,method:`POST`})},DELETE(e,t){return d(e,{...t,method:`DELETE`})},OPTIONS(e,t){return d(e,{...t,method:`OPTIONS`})},HEAD(e,t){return d(e,{...t,method:`HEAD`})},PATCH(e,t){return d(e,{...t,method:`PATCH`})},TRACE(e,t){return d(e,{...t,method:`TRACE`})},use(...e){for(let t of e)if(t){if(typeof t!=`object`||!(`onRequest`in t||`onResponse`in t||`onError`in t))throw Error("Middleware must be an object with one of `onRequest()`, `onResponse() or `onError()`");u.push(t)}},eject(...e){for(let t of e){let e=u.indexOf(t);e!==-1&&u.splice(e,1)}}}}function z(e,t,n){if(t==null)return``;if(typeof t==`object`)throw Error("Deeply-nested arrays/objects aren’t supported. Provide your own `querySerializer()` to handle these.");return`${e}=${n?.allowReserved===!0?t:encodeURIComponent(t)}`}function _t(e,t,n){if(!t||typeof t!=`object`)return``;let r=[],i={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`;if(n.style!==`deepObject`&&n.explode===!1){for(let e in t)r.push(e,n.allowReserved===!0?t[e]:encodeURIComponent(t[e]));let i=r.join(`,`);switch(n.style){case`form`:return`${e}=${i}`;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return i}}for(let i in t){let a=n.style===`deepObject`?`${e}[${i}]`:i;r.push(z(a,t[i],n))}let a=r.join(i);return n.style===`label`||n.style===`matrix`?`${i}${a}`:a}function vt(e,t,n){if(!Array.isArray(t))return``;if(n.explode===!1){let r={form:`,`,spaceDelimited:`%20`,pipeDelimited:`|`}[n.style]||`,`,i=(n.allowReserved===!0?t:t.map(e=>encodeURIComponent(e))).join(r);switch(n.style){case`simple`:return i;case`label`:return`.${i}`;case`matrix`:return`;${e}=${i}`;default:return`${e}=${i}`}}let r={simple:`,`,label:`.`,matrix:`;`}[n.style]||`&`,i=[];for(let r of t)n.style===`simple`||n.style===`label`?i.push(n.allowReserved===!0?r:encodeURIComponent(r)):i.push(z(e,r,n));return n.style===`label`||n.style===`matrix`?`${r}${i.join(r)}`:i.join(r)}function yt(e){return function(t){let n=[];if(t&&typeof t==`object`)for(let r in t){let i=t[r];if(i!=null){if(Array.isArray(i)){if(i.length===0)continue;n.push(vt(r,i,{style:`form`,explode:!0,...e?.array,allowReserved:e?.allowReserved||!1}));continue}if(typeof i==`object`){n.push(_t(r,i,{style:`deepObject`,explode:!0,...e?.object,allowReserved:e?.allowReserved||!1}));continue}n.push(z(r,i,e))}}return n.join(`&`)}}function bt(e,t){let n=e;for(let r of e.match(Tt)??[]){let e=r.substring(1,r.length-1),i=!1,a=`simple`;if(e.endsWith(`*`)&&(i=!0,e=e.substring(0,e.length-1)),e.startsWith(`.`)?(a=`label`,e=e.substring(1)):e.startsWith(`;`)&&(a=`matrix`,e=e.substring(1)),!t||t[e]===void 0||t[e]===null)continue;let o=t[e];if(Array.isArray(o)){n=n.replace(r,vt(e,o,{style:a,explode:i}));continue}if(typeof o==`object`){n=n.replace(r,_t(e,o,{style:a,explode:i}));continue}if(a===`matrix`){n=n.replace(r,`;${z(e,o)}`);continue}n=n.replace(r,a===`label`?`.${encodeURIComponent(o)}`:encodeURIComponent(o))}return n}function xt(e,t){return e instanceof FormData?e:t&&(t.get instanceof Function?t.get(`Content-Type`)??t.get(`content-type`):t[`Content-Type`]??t[`content-type`])===`application/x-www-form-urlencoded`?new URLSearchParams(e).toString():JSON.stringify(e)}function St(e,t){let n=`${t.baseUrl}${e}`;t.params?.path&&(n=t.pathSerializer(n,t.params.path));let r=t.querySerializer(t.params.query??{});return r.startsWith(`?`)&&(r=r.substring(1)),r&&(n+=`?${r}`),n}function Ct(...e){let t=new Headers;for(let n of e){if(!n||typeof n!=`object`)continue;let e=n instanceof Headers?n.entries():Object.entries(n);for(let[n,r]of e)if(r===null)t.delete(n);else if(Array.isArray(r))for(let e of r)t.append(n,e);else r!==void 0&&t.set(n,r)}return t}function wt(e){return e.endsWith(`/`)?e.substring(0,e.length-1):e}var Tt,Et;function Dt(){return(Dt=e((()=>{Tt=/\{[^{}]+\}/g,Et=()=>typeof process==`object`&&Number.parseInt(process?.versions?.node?.substring(0,2))>=18&&process.versions.undici})))()}function Ot(e){if(!e||typeof e!=`object`||Array.isArray(e))return{};let t=e,n=t.status===`error`&&t.details&&typeof t.details==`object`&&!Array.isArray(t.details)?t.details:t,r={};for(let[e,i]of Object.entries(n))if(!(n===t&&jt.has(e))){if(Array.isArray(i)){let t=i.filter(e=>typeof e==`string`);t.length>0&&(r[e]=t)}else typeof i==`string`&&(r[e]=[i])}return r}var B,kt,At,jt;function Mt(){return(Mt=e((()=>{B=class extends Error{status;statusText;data;constructor(e,t,n){super(`HTTP ${e}: ${t}`),this.status=e,this.statusText=t,this.data=n,this.name=`HttpError`}},kt=class extends Error{cause;constructor(e){super(`Network request failed`),this.cause=e,this.name=`NetworkError`}},At=class extends B{fieldErrors;constructor(e,t,n,r){super(e,t,n),this.fieldErrors=r,this.name=`ValidationError`}},jt=new Set([`detail`,`status`,`message`,`type`])})))()}function Nt(){let e=document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);return e?decodeURIComponent(e[1]):``}function Pt(){let e=encodeURIComponent(window.location.pathname+window.location.search);throw window.location.href=`/utilisateur/connexion?next=${e}`,Error(`Redirecting to login`)}function Ft(e){let t=[`GET`,`POST`,`PUT`,`PATCH`,`DELETE`,`HEAD`,`OPTIONS`,`TRACE`],n={...e};for(let r of t){let t=e[r];n[r]=async(...e)=>{try{return await t(...e)}catch(e){throw e instanceof DOMException&&e.name===`AbortError`||e instanceof B||e instanceof Error&&e.message===`Redirecting to login`?e:new kt(e)}}}return n}var It,Lt,V;function Rt(){return(Rt=e((()=>{Dt(),Mt(),It={async onRequest({request:e}){if(e.method!==`GET`)return e.headers.set(`X-CSRFToken`,Nt()),e}},Lt={async onResponse({response:e}){if(e.ok)return;e.status===401&&Pt();let t=await e.clone().json().catch(()=>void 0);throw e.status===400||e.status===422?new At(e.status,e.statusText,t,Ot(t)):new B(e.status,e.statusText,t)}},V=gt({baseUrl:typeof window<`u`?window.location.origin:``,credentials:`same-origin`,fetch:(...e)=>globalThis.fetch(...e)}),V.use(It),V.use(Lt),Ft(V)})))()}function zt(){let e=document.createElement(`form`);e.method=`POST`,e.action=`/utilisateur/deconnexion`,e.hidden=!0;let t=document.createElement(`input`);t.type=`hidden`,t.name=`csrfmiddlewaretoken`,t.value=Nt(),e.append(t),document.body.append(e),e.submit()}function Bt(){return(Bt=e((()=>{Rt()})))()}var Vt,Ht,Ut,Wt,Gt,H;function Kt(){return(Kt=e((()=>{b(),le(),E(),M(),Vt=[`aria-label`],Ht={class:`csp-sidebar-dropdown-button__leading`},Ut={class:`csp-sidebar-dropdown-button__text`},Wt={class:`csp-sidebar-dropdown-button__title`},Gt={key:0,class:`csp-sidebar-dropdown-button__description`},H=f({inheritAttrs:!1,__name:`CspSidebarDropdown`,props:{sections:{},align:{},side:{},sideOffset:{},sideFlip:{type:Boolean},title:{},description:{}},setup(e){let t=e,r=y(()=>{let{title:e,description:n,...r}=t;return r}),{showLabels:o}=j();return(t,d)=>(l(),h(ue,s(n(r.value)),{trigger:S(()=>[w(`button`,u({type:`button`,class:`csp-sidebar-dropdown-button`,"aria-label":e.title},t.$attrs),[w(`span`,Ht,[c(t.$slots,`leading`,{},void 0,!0)]),g(o)?(l(),C(ee,{key:0},[w(`span`,Ut,[w(`span`,Wt,p(e.title),1),e.description?(l(),C(`span`,Gt,p(e.description),1)):i(``,!0)]),a(D,{name:`ri:expand-up-down-line`,size:16,class:`csp-sidebar-dropdown-button__chevron`})],64)):i(``,!0)],16,Vt)]),_:3},16))}})})))()}var qt;function Jt(){return(Jt=e((()=>{Kt(),O(),qt=k(H,[[`__scopeId`,`data-v-363aabcf`]]),H.__docgenInfo=Object.assign({displayName:H.name??H.__name},{exportName:`default`,displayName:`CspSidebarDropdown`,type:1,props:[],events:[],slots:[{name:`leading`,description:``,type:`{}`,schema:`{}`,tags:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarDropdown.vue`})})))()}function Yt(){return typeof window>`u`?!1:window.matchMedia(`(prefers-color-scheme: dark)`).matches}function U(e){typeof document>`u`||document.documentElement.setAttribute(`data-fr-theme`,e?`dark`:`light`)}function Xt(){let e=y(()=>W.value===`system`?G.value:W.value===`dark`);function n(t){W.value=t,localStorage.setItem(Zt,t),U(e.value)}function i(){n(e.value?`light`:`dark`)}let a=null,o=null;return T(()=>{G.value=Yt();let t=localStorage.getItem(Zt);t&&[`light`,`dark`,`system`].includes(t)&&(W.value=t),U(e.value),a=window.matchMedia(`(prefers-color-scheme: dark)`),o=e=>{G.value=e.matches,W.value===`system`&&U(e.matches)},a.addEventListener(`change`,o)}),r(()=>{a&&o&&a.removeEventListener(`change`,o)}),t(e,e=>{U(e)}),{colorMode:W,isDark:e,setColorMode:n,toggle:i}}var Zt,W,G;function Qt(){return(Qt=e((()=>{b(),Zt=`csp_color_mode`,W=x(`system`),G=x(!1)})))()}var K;function $t(){return($t=e((()=>{b(),Bt(),A(),Jt(),Qt(),K=f({__name:`CspSidebarUser`,props:{name:{},role:{}},setup(e){let{isDark:t,toggle:n}=Xt();return(r,i)=>(l(),h(qt,{align:`end`,side:`right`,title:e.name,description:e.role,"aria-label":`Compte : ${e.name}`,sections:[{items:[{label:g(t)?`Mode clair`:`Mode sombre`,icon:g(t)?`ri:sun-line`:`ri:moon-line`,onSelect:g(n)}]},{items:[{label:`Mon profil`,icon:`ri:user-line`},{label:`Paramètres`,icon:`ri:settings-3-line`}]},{items:[{label:`Se déconnecter`,icon:`ri:logout-box-r-line`,destructive:!0,onSelect:g(zt)}]}]},{leading:S(()=>[a(ie,{name:e.name},null,8,[`name`])]),_:1},8,[`title`,`description`,`aria-label`,`sections`]))}})})))()}var en;function tn(){return(tn=e((()=>{$t(),en=K,K.__docgenInfo=Object.assign({displayName:K.name??K.__name},{exportName:`default`,displayName:`CspSidebarUser`,type:1,props:[{name:`name`,global:!1,description:``,tags:[],required:!0,type:`string`,schema:`string`,declarations:[]},{name:`role`,global:!1,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarUser.vue`})})))()}var nn,q,J,Y,X,Z,Q,$,rn;function an(){return(an=e((()=>{te(),ae(),Ce(),Je(),$e(),rt(),ct(),dt(),mt(),tn(),nn={title:`Compositions/Génériques/CspSidebar`,component:ut,parameters:{layout:`fullscreen`,docs:{description:{component:"\nSidebar de navigation adaptée au DSFR.\n\n## Composants\n\n- `CspSidebarProvider` : contexte partagé (état, mobile, raccourcis)\n- `CspSidebar` : panneau de navigation\n- `CspSidebarTrigger` : bouton hamburger mobile (dans le header)\n- `CspSidebarGroup`, `CspSidebarItem`, `CspSidebarLogo`, `CspSidebarUser`\n\n## Slots\n\n- `logo` : en-tête, à la hauteur du fil d'Ariane de la page\n- `context` : sous l'en-tête, à la hauteur du titre de la page (sélecteur d'espace ou d'organisme)\n- défaut : entrées de navigation, groupées par `CspSidebarGroup`\n- `footer` : bas de panneau (utilisateur)\n\n## Usage\n\n```vue\n<CspAppShell :navigation=\"navigation\">\n  <!-- contenu de page -->\n</CspAppShell>\n```\n        "}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},q=`
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
`,J={CspSidebar:qe,CspSidebarGroup:Qe,CspSidebarItem:nt,CspSidebarLogo:st,CspSidebarProvider:ut,CspSidebarTrigger:pt,CspSidebarUser:en},Y={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:J,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:q})},X={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:J,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:q})},Z={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:J,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:q})},Q={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:J,setup(){let t=re();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
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
    `})},$={name:`Avec sélecteur de contexte`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Le slot `context` reçoit un sélecteur d'espace ou d'organisme, à la hauteur du titre de la page ; la navigation commence sous la ligne de l'en-tête. La zone est réservée même sans contenu."}}},render:e=>({components:{...J,CspSelect:oe,CspPageHeader:we},setup(){return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,options:[{value:`a`,label:`Premier espace`},{value:`b`,label:`Deuxième espace`}],breadcrumb:[{label:`Accueil`,to:`/`},{label:`Page`}]}},template:`
      <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
        <div style="display: flex; min-height: 100vh;">
          <aside style="flex-shrink: 0; border-right: 1px solid var(--border-default-grey);">
            <CspSidebar>
              <template #logo>
                <CspSidebarLogo />
              </template>

              <template #context>
                <CspSelect :options="options" model-value="a" aria-label="Espace" />
              </template>

              <CspSidebarGroup>
                <CspSidebarItem icon="ri:briefcase-line" label="Entrée active" :to="{ path: '/active' }" :is-active="true" />
                <CspSidebarItem icon="ri:group-line" label="Deuxième entrée" :to="{ path: '/deuxieme' }" />
              </CspSidebarGroup>

              <CspSidebarGroup>
                <CspSidebarItem icon="ri:settings-3-line" label="Troisième entrée" :to="{ path: '/troisieme' }" />
              </CspSidebarGroup>

              <template #footer>
                <CspSidebarUser name="Prénom Nom" role="Rôle" />
              </template>
            </CspSidebar>
          </aside>

          <div style="flex: 1; min-width: 0;">
            <CspPageHeader title="Titre de la page" :breadcrumb="breadcrumb">
              <template #subtitle>
                <p style="margin: 0; color: var(--text-mention-grey);">Sous-titre de la page</p>
              </template>
            </CspPageHeader>
          </div>
        </div>
      </CspSidebarProvider>
    `})},rn=[`Default`,`Collapsed`,`Mobile`,`WithRouterLinks`,`WithContext`],Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
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
}`,...Q.parameters?.docs?.source}}},$.parameters={...$.parameters,docs:{...$.parameters?.docs,source:{originalSource:`{
  name: 'Avec sélecteur de contexte',
  args: {
    defaultExpanded: true,
    persistState: false
  },
  parameters: {
    docs: {
      description: {
        story: 'Le slot \`context\` reçoit un sélecteur d\\'espace ou d\\'organisme, à la hauteur du titre de la page ; la navigation commence sous la ligne de l\\'en-tête. La zone est réservée même sans contenu.'
      }
    }
  },
  render: args => ({
    components: {
      ...components,
      CspSelect,
      CspPageHeader
    },
    setup() {
      const options = [{
        value: 'a',
        label: 'Premier espace'
      }, {
        value: 'b',
        label: 'Deuxième espace'
      }];
      const breadcrumb = [{
        label: 'Accueil',
        to: '/'
      }, {
        label: 'Page'
      }];
      return {
        defaultExpanded: args.defaultExpanded,
        persistState: args.persistState,
        options,
        breadcrumb
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

              <template #context>
                <CspSelect :options="options" model-value="a" aria-label="Espace" />
              </template>

              <CspSidebarGroup>
                <CspSidebarItem icon="ri:briefcase-line" label="Entrée active" :to="{ path: '/active' }" :is-active="true" />
                <CspSidebarItem icon="ri:group-line" label="Deuxième entrée" :to="{ path: '/deuxieme' }" />
              </CspSidebarGroup>

              <CspSidebarGroup>
                <CspSidebarItem icon="ri:settings-3-line" label="Troisième entrée" :to="{ path: '/troisieme' }" />
              </CspSidebarGroup>

              <template #footer>
                <CspSidebarUser name="Prénom Nom" role="Rôle" />
              </template>
            </CspSidebar>
          </aside>

          <div style="flex: 1; min-width: 0;">
            <CspPageHeader title="Titre de la page" :breadcrumb="breadcrumb">
              <template #subtitle>
                <p style="margin: 0; color: var(--text-mention-grey);">Sous-titre de la page</p>
              </template>
            </CspPageHeader>
          </div>
        </div>
      </CspSidebarProvider>
    \`
  })
}`,...$.parameters?.docs?.source}}}})))()}an();export{X as Collapsed,Y as Default,Z as Mobile,$ as WithContext,Q as WithRouterLinks,rn as __namedExportsOrder,nn as default};