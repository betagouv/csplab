import{n as e}from"./rolldown-runtime-sJBDdmOt.js";import{$ as t,C as n,D as r,E as i,F as a,Ot as o,P as s,Q as ee,S as c,St as l,T as te,U as u,V as d,W as f,X as ne,Y as re,a as p,b as m,c as h,g,ht as ie,rt as _,s as v,x as y,y as b}from"./iframe-Crr-5wH-.js";import{n as x,t as ae}from"./CspIcon-Bsr2NDRn.js";import{n as S,t as C}from"./_plugin-vue_export-helper-ktEZWxTd.js";import{a as oe,c as se,i as ce,l as le,n as w,o as ue,r as de,s as fe,t as pe}from"./ListboxItem-CJDa_uHl.js";import{E as me,T as he,n as ge,t as _e}from"./useForwardExpose-BHtLJ0ry.js";import{n as T,t as E}from"./Primitive-8uCJ-Nfu.js";import{n as ve,t as ye}from"./useId-C9Dm73lD.js";import{n as be,t as xe}from"./CspPopover-CGRZcsaM.js";import{n as Se,t as Ce}from"./CspButton-wDVqpUPs.js";import{n as we,t as Te}from"./CspAvatar-DUKrgcdQ.js";import{a as D,c as Ee,d as De,f as Oe,g as ke,h as Ae,i as je,l as Me,m as Ne,n as Pe,o as Fe,p as Ie,r as O,s as Le,t as Re,u as ze}from"./CspSidebarUser-DYY5Dmti.js";import{n as Be,t as Ve}from"./CspPageHeader-BABisXJ4.js";var k,A,j;function M(){return(M=e((()=>{me(),ye(),T(),h(),[k,A]=he(`ListboxGroup`),j=r({__name:`ListboxGroup`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){let t=e,n=ve(void 0,`reka-listbox-group`);return A({id:n}),(e,r)=>(d(),y(l(E),a({role:`group`},t,{"aria-labelledby":l(n)}),{default:_(()=>[f(e.$slots,`default`)]),_:3},16,[`aria-labelledby`]))}})})))()}var N;function P(){return(P=e((()=>{T(),M(),h(),N=r({__name:`ListboxGroupLabel`,props:{for:{type:String,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`div`}},setup(e){let t=e,n=k({id:``});return(e,r)=>(d(),y(l(E),a(t,{id:l(n).id}),{default:_(()=>[f(e.$slots,`default`)]),_:3},16,[`id`]))}})})))()}var F;function I(){return(I=e((()=>{_e(),T(),w(),h(),F=r({__name:`ListboxItemIndicator`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`span`}},setup(e){let t=e;ge();let n=de();return(e,r)=>l(n).isSelected.value?(d(),y(l(E),a({key:0,"aria-hidden":`true`},t),{default:_(()=>[f(e.$slots,`default`)]),_:3},16)):c(`v-if`,!0)}})})))()}var He,Ue,We,Ge,Ke,qe,Je,L;function Ye(){return(Ye=e((()=>{h(),fe(),oe(),M(),P(),w(),I(),le(),x(),be(),je(),He={class:`csp-sidebar-switcher__filter`},Ue=[`for`],We={class:`csp-sidebar-switcher__filter-field`},Ge={key:0,class:`csp-sidebar-switcher__separator`,"aria-hidden":`true`},Ke={class:`csp-sidebar-switcher__option-text`},qe={key:0,class:`csp-sidebar-switcher__option-description`},Je={class:`csp-sidebar-switcher__empty`,role:`status`},L=r({inheritAttrs:!1,__name:`CspSidebarSwitcher`,props:s({title:{},groups:{},selected:{default:null},filterLabel:{default:void 0},filterPlaceholder:{default:void 0},emptyLabel:{default:`Aucun résultat`}},{search:{default:``},searchModifiers:{}}),emits:s([`select`],[`update:search`]),setup(e,{emit:r}){let s=e,p=r,h=ne(e,`search`),v=ie(!1),x=re(),S=b(()=>s.groups.filter(e=>e.options.length>0)),C=b(()=>S.value.reduce((e,t)=>e+t.options.length,0)),oe=b(()=>!s.filterLabel&&C.value<=1),le=b(()=>v.value&&C.value===0?s.emptyLabel:``);t(v,e=>{e||(h.value=``)});let w=ee(`listbox`);t(()=>s.groups,()=>{h.value&&w.value?.highlightFirstItem()});function de(e){v.value=!1,p(`select`,e)}return(t,r)=>oe.value?(d(),y(O,{key:0,static:``,title:e.title},{leading:_(()=>[f(t.$slots,`leading`,{},void 0,!0)]),_:3},8,[`title`])):(d(),y(xe,{key:1,open:v.value,"onUpdate:open":r[1]||=e=>v.value=e,side:`bottom`,align:`start`,padding:`menu`},{trigger:_(()=>[i(O,a({title:e.title},t.$attrs),{leading:_(()=>[f(t.$slots,`leading`,{},void 0,!0)]),_:3},16,[`title`])]),default:_(()=>[i(l(se),{ref_key:`listbox`,ref:w,class:`csp-sidebar-switcher`,"model-value":e.selected??void 0,"highlight-on-hover":``},{default:_(()=>[e.filterLabel?(d(),n(g,{key:0},[m(`div`,He,[m(`label`,{for:l(x),class:`csp-sidebar-switcher__label`},o(e.filterLabel),9,Ue),m(`span`,We,[i(ae,{name:`ri:search-line`,class:`csp-sidebar-switcher__filter-icon`,"aria-hidden":`true`}),i(l(ce),{id:l(x),modelValue:h.value,"onUpdate:modelValue":r[0]||=e=>h.value=e,type:`search`,autocomplete:`off`,class:`csp-sidebar-switcher__filter-input`,placeholder:e.filterPlaceholder,"auto-focus":``},null,8,[`id`,`modelValue`,`placeholder`])])]),r[2]||=m(`div`,{class:`csp-sidebar-switcher__separator`,"aria-hidden":`true`},null,-1)],64)):c(``,!0),i(l(ue),{class:`csp-sidebar-switcher__content`},{default:_(()=>[(d(!0),n(g,null,u(S.value,(e,t)=>(d(),n(g,{key:e.label??t},[t>0?(d(),n(`div`,Ge)):c(``,!0),i(l(j),null,{default:_(()=>[e.label?(d(),y(l(N),{key:0,class:`csp-sidebar-switcher__label csp-sidebar-switcher__group-label`},{default:_(()=>[te(o(e.label),1)]),_:2},1024)):c(``,!0),(d(!0),n(g,null,u(e.options,e=>(d(),y(l(pe),{key:e.value,value:e.value,class:`csp-sidebar-switcher__option`,onSelect:t=>de(e.value)},{default:_(()=>[m(`span`,Ke,[m(`span`,null,o(e.label),1),e.description?(d(),n(`span`,qe,o(e.description),1)):c(``,!0)]),i(l(F),{class:`csp-sidebar-switcher__option-indicator`},{default:_(()=>[i(ae,{name:`ri:check-line`})]),_:1})]),_:2},1032,[`value`,`onSelect`]))),128))]),_:2},1024)],64))),128))]),_:1}),m(`p`,Je,o(le.value),1)]),_:1},8,[`model-value`])]),_:3},8,[`open`]))}})})))()}var Xe;function Ze(){return(Ze=e((()=>{Ye(),S(),Xe=C(L,[[`__scopeId`,`data-v-6a0eddf9`]]),L.__docgenInfo=Object.assign({displayName:L.name??L.__name},{exportName:`default`,displayName:`CspSidebarSwitcher`,type:1,props:[{name:`title`,global:!1,description:``,tags:[],required:!0,type:`string`,schema:`string`,declarations:[]},{name:`groups`,global:!1,description:``,tags:[],required:!0,type:`CspSidebarSwitcherGroup[]`,schema:{kind:`array`,type:`CspSidebarSwitcherGroup[]`},declarations:[]},{name:`selected`,global:!1,default:`null`,description:``,tags:[],required:!1,type:`string | null | undefined`,schema:{kind:`enum`,type:`string | null | undefined`,schema:[`undefined`,`null`,`string`]},declarations:[]},{name:`filterLabel`,global:!1,default:`undefined`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`filterPlaceholder`,global:!1,default:`undefined`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`emptyLabel`,global:!1,default:`"Aucun résultat"`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`search`,global:!1,default:`""`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[{name:`update:search`,description:``,tags:[],type:`[value: string]`,signature:`(event: "update:search", value: string): void`,schema:[`string`],declarations:[]},{name:`select`,description:``,tags:[],type:`[value: string]`,signature:`(event: "select", value: string): void`,schema:[`string`],declarations:[]}],slots:[{name:`leading`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarSwitcher.vue`})})))()}var R;function Qe(){return(Qe=e((()=>{h(),Se(),Ae(),R=r({__name:`CspSidebarTrigger`,setup(e){let{toggle:t,isMobile:n}=ke();return(e,r)=>l(n)?(d(),y(Ce,{key:0,variant:`tertiary-no-outline`,size:`sm`,icon:`ri:menu-line`,"aria-label":`Ouvrir le menu`,onClick:l(t)},null,8,[`onClick`])):c(``,!0)}})})))()}var $e;function et(){return(et=e((()=>{Qe(),$e=R,R.__docgenInfo=Object.assign({displayName:R.name??R.__name},{exportName:`default`,displayName:`CspSidebarTrigger`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarTrigger.vue`})})))()}function z(e,t){return{args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:t}}},render:t=>({components:{...H,CspAvatar:Te,CspSidebarSwitcher:Xe,CspPageHeader:Ve},setup(){let n=ie(``),r=b(()=>e.groupsFor(n.value)),i=[{label:`Accueil`,to:`/`},{label:`Page`}],a=`${e.title}. Changer d'espace`;return{defaultExpanded:t.defaultExpanded,persistState:t.persistState,switcher:e,ariaLabel:a,search:n,groups:r,breadcrumb:i}},template:`
        <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
          <div style="display: flex; min-height: 100vh;">
            <aside style="flex-shrink: 0; border-right: 1px solid var(--border-default-grey);">
              <CspSidebar>
                <template #logo>
                  <CspSidebarLogo />
                </template>

                <template #context>
                  <CspSidebarSwitcher
                    v-model:search="search"
                    :title="switcher.title"
                    :groups="groups"
                    :selected="switcher.selected"
                    :filter-label="switcher.filterLabel"
                    :aria-label="ariaLabel"
                  >
                    <template #leading>
                      <CspAvatar icon="ri:government-fill" />
                    </template>
                  </CspSidebarSwitcher>
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
      `})}}var B,V,H,U,W,G,K,q,J,Y,X,Z,Q,tt;function $(){return($=e((()=>{h(),p(),we(),Be(),Ne(),Oe(),ze(),Ee(),Fe(),Ze(),et(),Pe(),B={title:`Compositions/Génériques/CspSidebar`,component:D,parameters:{layout:`fullscreen`,docs:{description:{component:"\nSidebar de navigation adaptée au DSFR.\n\n## Composants\n\n- `CspSidebarProvider` : contexte partagé (état, mobile, raccourcis)\n- `CspSidebar` : panneau de navigation\n- `CspSidebarTrigger` : bouton hamburger mobile (dans le header)\n- `CspSidebarGroup`, `CspSidebarItem`, `CspSidebarLogo`, `CspSidebarUser`\n- `CspSidebarSwitcher` : sélecteur d'espace, avec recherche facultative ; un bloc fixe quand la liste a un seul choix et aucune recherche\n\n## Slots\n\n- `logo` : en-tête, à la hauteur du fil d'Ariane de la page\n- `context` : sous l'en-tête, à la hauteur du titre de la page (sélecteur d'espace ou d'organisme)\n- défaut : entrées de navigation, groupées par `CspSidebarGroup`\n- `footer` : bas de panneau (utilisateur)\n\n## Usage\n\n```vue\n<CspAppShell :navigation=\"navigation\">\n  <!-- contenu de page -->\n</CspAppShell>\n```\n        "}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},V=`
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
`,H={CspSidebar:Ie,CspSidebarGroup:De,CspSidebarItem:Me,CspSidebarLogo:Le,CspSidebarProvider:D,CspSidebarTrigger:$e,CspSidebarUser:Re},U={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:H,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:V})},W={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:H,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:V})},G={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:H,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:V})},K={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:H,setup(){let t=v();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
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
    `})},q={value:`atelier`,label:`Atelier des Hautes-Alpes`},J={value:`cooperative`,label:`Coopérative des producteurs de la vallée de la Haute-Durance`},Y=[q,J,{value:`association`,label:`Association des usagers du réseau de transport`}],X={name:`Avec sélecteur de contexte`,...z({title:J.label,selected:J.value,groupsFor:()=>[{label:`Changer d'espace`,options:Y}]},"Le slot `context` reçoit un sélecteur d'espace ou d'organisme, à la hauteur du titre de la page ; la navigation commence sous la ligne de l'en-tête. La zone est réservée même sans contenu.")},Z={name:`Avec sélecteur de contexte et recherche`,...z({title:`Vue d'ensemble`,selected:`ensemble`,filterLabel:`Rechercher un espace`,groupsFor:e=>{let t=e.trim().toLowerCase();return t?[{options:Y.filter(e=>e.label.toLowerCase().includes(t))}]:[{options:[{value:`ensemble`,label:`Vue d'ensemble`}]},{label:`Récents`,options:[q,J]}]}},"Avec `filterLabel`, le menu commence par un champ de recherche ; le parent filtre les groupes à partir de `v-model:search`. Le sélecteur vide la recherche à la fermeture.")},Q={name:`Avec un seul contexte`,...z({title:q.label,selected:q.value,groupsFor:()=>[{options:[q]}]},`Avec un seul choix et sans recherche, le sélecteur devient un bloc fixe, sans menu.`)},tt=[`Default`,`Collapsed`,`Mobile`,`WithRouterLinks`,`WithContext`,`WithSearchableContext`,`WithSingleContext`],U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{
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
}`,...U.parameters?.docs?.source}}},W.parameters={...W.parameters,docs:{...W.parameters?.docs,source:{originalSource:`{
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
}`,...W.parameters?.docs?.source}}},G.parameters={...G.parameters,docs:{...G.parameters?.docs,source:{originalSource:`{
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
}`,...G.parameters?.docs?.source}}},K.parameters={...K.parameters,docs:{...K.parameters?.docs,source:{originalSource:`{
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
}`,...K.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  name: 'Avec sélecteur de contexte',
  ...contextStory({
    title: COOPERATIVE.label,
    selected: COOPERATIVE.value,
    groupsFor: () => [{
      label: 'Changer d\\'espace',
      options: ESPACES
    }]
  }, 'Le slot \`context\` reçoit un sélecteur d\\'espace ou d\\'organisme, à la hauteur du titre de la page ; la navigation commence sous la ligne de l\\'en-tête. La zone est réservée même sans contenu.')
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  name: 'Avec sélecteur de contexte et recherche',
  ...contextStory({
    title: 'Vue d\\'ensemble',
    selected: 'ensemble',
    filterLabel: 'Rechercher un espace',
    groupsFor: search => {
      const term = search.trim().toLowerCase();
      if (term) {
        return [{
          options: ESPACES.filter(espace => espace.label.toLowerCase().includes(term))
        }];
      }
      return [{
        options: [{
          value: 'ensemble',
          label: 'Vue d\\'ensemble'
        }]
      }, {
        label: 'Récents',
        options: [ATELIER, COOPERATIVE]
      }];
    }
  }, 'Avec \`filterLabel\`, le menu commence par un champ de recherche ; le parent filtre les groupes à partir de \`v-model:search\`. Le sélecteur vide la recherche à la fermeture.')
}`,...Z.parameters?.docs?.source}}},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
  name: 'Avec un seul contexte',
  ...contextStory({
    title: ATELIER.label,
    selected: ATELIER.value,
    groupsFor: () => [{
      options: [ATELIER]
    }]
  }, 'Avec un seul choix et sans recherche, le sélecteur devient un bloc fixe, sans menu.')
}`,...Q.parameters?.docs?.source}}}})))()}$();export{W as Collapsed,U as Default,G as Mobile,X as WithContext,K as WithRouterLinks,Z as WithSearchableContext,Q as WithSingleContext,tt as __namedExportsOrder,B as default};