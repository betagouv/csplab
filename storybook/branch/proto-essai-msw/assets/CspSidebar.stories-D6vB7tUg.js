import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{W as t,_ as n,b as r,g as i,q as a,t as o,yt as s}from"./vue.esm-bundler-BdiU-5Kf.js";import{h as c}from"./useApi-CROJJdhE-BkknRUWw.js";import{q as l}from"./iframe-DaA6_v4-.js";import{a as u,c as d,d as f,f as p,i as m,l as h,m as g,n as _,o as v,p as y,r as b,s as x,t as S,u as C}from"./CspSidebarSwitcher-U08iPPB0.js";import{n as w,t as T}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as E,t as D}from"./CspAvatar-DBkp4RK8.js";import{n as O,t as k}from"./CspPageHeader-iOHJFNr4.js";function A(e,i){return t(),r(`div`,M,[n(`div`,N,[a(e.$slots,`default`,{},void 0,!0)])])}var j,M,N,P;function F(){return(F=e((()=>{o(),w(),j={},M={class:`csp-sidebar-group`},N={class:`csp-sidebar-group__items`},P=T(j,[[`render`,A],[`__scopeId`,`data-v-99e3ccf5`]]),j.__docgenInfo=Object.assign({displayName:j.name??j.__name},{exportName:`default`,displayName:`CspSidebarGroup`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[{name:`default`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/layout/CspSidebar/CspSidebarGroup.vue`})})))()}function I(e,t){return{args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:t}}},render:t=>({components:{...z,CspAvatar:D,CspSidebarSwitcher:S,CspPageHeader:k},setup(){let n=s(``),r=i(()=>e.groupsFor(n.value)),a=[{label:`Accueil`,to:`/`},{label:`Page`}],o=`${e.title}. Changer d'espace`;return{defaultExpanded:t.defaultExpanded,persistState:t.persistState,switcher:e,ariaLabel:o,search:n,groups:r,breadcrumb:a}},template:`
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
      `})}}var L,R,z,B,V,H,U,W,G,K,q,J,Y,X;function Z(){return(Z=e((()=>{o(),l(),E(),O(),g(),F(),p(),C(),d(),_(),v(),m(),L={title:`Compositions/Génériques/CspSidebar`,component:x,parameters:{layout:`fullscreen`,docs:{description:{component:"\nSidebar de navigation adaptée au DSFR.\n\n## Composants\n\n- `CspSidebarProvider` : contexte partagé (état, mobile, raccourcis)\n- `CspSidebar` : panneau de navigation\n- `CspSidebarTrigger` : bouton hamburger mobile (dans le header)\n- `CspSidebarGroup`, `CspSidebarItem`, `CspSidebarLogo`, `CspSidebarUser`\n- `CspSidebarSwitcher` : sélecteur d'espace, avec recherche facultative ; un bloc fixe quand la liste a un seul choix et aucune recherche\n\n## Slots\n\n- `logo` : en-tête, à la hauteur du fil d'Ariane de la page\n- `context` : sous l'en-tête, à la hauteur du titre de la page (sélecteur d'espace ou d'organisme)\n- défaut : entrées de navigation, groupées par `CspSidebarGroup`\n- `footer` : bas de panneau (utilisateur)\n\n## Usage\n\n```vue\n<CspAppShell :navigation=\"navigation\">\n  <!-- contenu de page -->\n</CspAppShell>\n```\n        "}}},argTypes:{defaultExpanded:{control:`boolean`,description:`État initial de la sidebar (ouverte ou fermée)`},persistState:{control:`boolean`,description:`Persister l'état en cookie`}}},R=`
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
`,z={CspSidebar:y,CspSidebarGroup:P,CspSidebarItem:f,CspSidebarLogo:h,CspSidebarProvider:x,CspSidebarTrigger:u,CspSidebarUser:b},B={args:{defaultExpanded:!0,persistState:!1},render:e=>({components:z,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:R})},V={args:{defaultExpanded:!1,persistState:!1},render:e=>({components:z,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:R})},H={args:{defaultExpanded:!0,persistState:!1},parameters:{viewport:{defaultViewport:`mobile1`}},render:e=>({components:z,setup:()=>({defaultExpanded:e.defaultExpanded,persistState:e.persistState}),template:R})},U={name:`Avec liens de navigation`,args:{defaultExpanded:!0,persistState:!1},parameters:{docs:{description:{story:"Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main."}}},render:e=>({components:z,setup(){let t=c();return{defaultExpanded:e.defaultExpanded,persistState:e.persistState,route:t,items:[{icon:`ri:dashboard-line`,label:`Première entrée`,to:`/premiere`},{icon:`ri:briefcase-line`,label:`Deuxième entrée`,to:`/deuxieme`},{icon:`ri:group-line`,label:`Troisième entrée`,to:`/troisieme`},{icon:`ri:settings-3-line`,label:`Quatrième entrée`,to:`/quatrieme`}]}},template:`
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
    `})},W={value:`atelier`,label:`Atelier des Hautes-Alpes`},G={value:`cooperative`,label:`Coopérative des producteurs de la vallée de la Haute-Durance`},K=[W,G,{value:`association`,label:`Association des usagers du réseau de transport`}],q={name:`Avec sélecteur de contexte`,...I({title:G.label,selected:G.value,groupsFor:()=>[{label:`Changer d'espace`,options:K}]},"Le slot `context` reçoit un sélecteur d'espace ou d'organisme, à la hauteur du titre de la page ; la navigation commence sous la ligne de l'en-tête. La zone est réservée même sans contenu.")},J={name:`Avec sélecteur de contexte et recherche`,...I({title:`Vue d'ensemble`,selected:`ensemble`,filterLabel:`Rechercher un espace`,groupsFor:e=>{let t=e.trim().toLowerCase();return t?[{options:K.filter(e=>e.label.toLowerCase().includes(t))}]:[{options:[{value:`ensemble`,label:`Vue d'ensemble`}]},{label:`Récents`,options:[W,G]}]}},"Avec `filterLabel`, le menu commence par un champ de recherche ; le parent filtre les groupes à partir de `v-model:search`. Le sélecteur vide la recherche à la fermeture.")},Y={name:`Avec un seul contexte`,...I({title:W.label,selected:W.value,groupsFor:()=>[{options:[W]}]},`Avec un seul choix et sans recherche, le sélecteur devient un bloc fixe, sans menu.`)},X=[`Default`,`Collapsed`,`Mobile`,`WithRouterLinks`,`WithContext`,`WithSearchableContext`,`WithSingleContext`],B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
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
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
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
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
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
}`,...H.parameters?.docs?.source}}},U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{
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
}`,...U.parameters?.docs?.source}}},q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{
  name: 'Avec sélecteur de contexte',
  ...contextStory({
    title: COOPERATIVE.label,
    selected: COOPERATIVE.value,
    groupsFor: () => [{
      label: 'Changer d\\'espace',
      options: ESPACES
    }]
  }, 'Le slot \`context\` reçoit un sélecteur d\\'espace ou d\\'organisme, à la hauteur du titre de la page ; la navigation commence sous la ligne de l\\'en-tête. La zone est réservée même sans contenu.')
}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
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
}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  name: 'Avec un seul contexte',
  ...contextStory({
    title: ATELIER.label,
    selected: ATELIER.value,
    groupsFor: () => [{
      options: [ATELIER]
    }]
  }, 'Avec un seul choix et sans recherche, le sélecteur devient un bloc fixe, sans menu.')
}`,...Y.parameters?.docs?.source}}}})))()}Z();export{V as Collapsed,B as Default,H as Mobile,q as WithContext,U as WithRouterLinks,J as WithSearchableContext,Y as WithSingleContext,X as __namedExportsOrder,L as default};