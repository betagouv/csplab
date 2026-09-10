import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{S as t,T as n,W as r,a as i,l as a,q as o,s}from"./iframe-C0OAurLG.js";import{n as c,t as l}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{a as u,c as d,d as f,f as p,i as m,l as h,n as g,o as _,r as v,s as y,t as b,u as x}from"./CspSidebarUser-DM9DoVVj.js";function S(e,i){return r(),n(`div`,w,[t(`div`,T,[o(e.$slots,`default`,{},void 0,!0)])])}var C,w,T,E;function D(){return(D=e((()=>{a(),c(),C={},w={class:`csp-sidebar-group`},T={class:`csp-sidebar-group__items`},E=l(C,[[`render`,S],[`__scopeId`,`data-v-a36d535a`]]),C.__docgenInfo=Object.assign({displayName:C.name??C.__name},{exportName:`default`,displayName:`CspSidebarGroup`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey`,schema:`PropertyKey`,declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef`,schema:`VNodeRef`,declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean`,schema:`boolean`,declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string`,schema:`string`,declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[]`,schema:`VNodeUpdateHook | VNodeUpdateHook[]`,declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[]`,schema:`VNodeUpdateHook | VNodeUpdateHook[]`,declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[]`,schema:`VNodeMountHook | VNodeMountHook[]`,declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[{name:`default`,type:`{}`,description:``,tags:[],schema:`{}`,declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarGroup.vue`})})))()}var O,k,A,j,M,N,P,F;function I(){return(I=e((()=>{i(),p(),D(),x(),d(),_(),m(),g(),O={title:`Compositions/Génériques/CspSidebar`,component:u,parameters:{layout:`fullscreen`,docs:{description:{component:'\nSidebar de navigation adaptée au DSFR.\n\n## Composants\n\n- `CspSidebarProvider` : contexte partagé (état, mobile, raccourcis)\n- `CspSidebar` : panneau de navigation\n- `CspSidebarTrigger` : bouton hamburger mobile (dans le header)\n- `CspSidebarGroup`, `CspSidebarItem`, `CspSidebarLogo`, `CspSidebarUser`\n\n## Usage\n\n```vue\n<CspAppShell :navigation="navigation">\n  <!-- contenu de page -->\n</CspAppShell>\n```\n        '}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},k=`
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
`,A={CspSidebar:f,CspSidebarGroup:E,CspSidebarItem:h,CspSidebarLogo:y,CspSidebarProvider:u,CspSidebarTrigger:v,CspSidebarUser:b},j={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:A,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:k})},M={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:A,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:k})},N={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:A,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:k})},P={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:A,setup(){let t=s();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
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
    `})},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
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
}`,...j.parameters?.docs?.source}}},M.parameters={...M.parameters,docs:{...M.parameters?.docs,source:{originalSource:`{
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
}`,...M.parameters?.docs?.source}}},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
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
}`,...N.parameters?.docs?.source}}},P.parameters={...P.parameters,docs:{...P.parameters?.docs,source:{originalSource:`{
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
}`,...P.parameters?.docs?.source}}},F=[`Default`,`Collapsed`,`Mobile`,`WithRouterLinks`]})))()}I();export{M as Collapsed,j as Default,N as Mobile,P as WithRouterLinks,F as __namedExportsOrder,O as default};