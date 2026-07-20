import{i as e}from"./preload-helper-Ct_ODC0V.js";import{At as t,D as n,Ot as r,gt as i}from"./iframe-9XWtStlm.js";import{n as a,t as o}from"./CspPagination-BArcSbTo.js";function s(e){return()=>({components:{CspPagination:o},setup(){return{demos:r(e.map(e=>({...e})))}},template:`
      <div class="flex flex-col gap-12 py-4">
        <section
          v-for="demo in demos"
          :key="demo.name"
          class="flex flex-col gap-2"
        >
          <p class="text-sm text-[var(--text-mention-grey)]">{{ demo.name }}</p>
          <CspPagination
            v-model:page="demo.page"
            :page-count="demo.pageCount"
            :sibling-count="demo.siblingCount"
            :show-first-last="demo.showFirstLast"
            :show-direction-labels="demo.showDirectionLabels"
            :disabled="demo.disabled"
          />
        </section>
      </div>
    `})}var c,l,u,d,f,p;e((()=>{n(),a(),c={title:`Éléments/Génériques/CspPagination`,component:o,tags:[`autodocs`],parameters:{controls:{include:[`page`,`pageCount`,`siblingCount`,`showFirstLast`,`showDirectionLabels`,`disabled`]},docs:{description:{component:"Pagination basée sur Reka UI et alignée sur les principes DSFR. Le composant expose une API contrôlée via `v-model:page` et gère la navigation clavier, les états désactivés et les attributs ARIA pour l’accessibilité."}}},argTypes:{page:{control:{type:`number`,min:1,step:1},description:`Page actuellement active.`,table:{type:{summary:`number`}}},pageCount:{control:{type:`number`,min:1,step:1},description:`Nombre total de pages disponibles.`,table:{type:{summary:`number`}}},siblingCount:{control:{type:`number`,min:0,step:1},description:`Nombre de pages voisines affichées autour de la page active.`,table:{type:{summary:`number`},defaultValue:{summary:`1`}}},showFirstLast:{control:{type:`boolean`},description:`Affiche les boutons de première et dernière page.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},showDirectionLabels:{control:{type:`boolean`},description:`Affiche les libellés de navigation « Précédente » et « Suivante » à partir du breakpoint large.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},disabled:{control:{type:`boolean`},description:`Désactive l’ensemble de la pagination.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{page:5,pageCount:12,siblingCount:1,showFirstLast:!0,showDirectionLabels:!0,disabled:!1},render:e=>({components:{CspPagination:o},setup(){let n=t(e.page??1);return i(()=>e.page,e=>{e!==void 0&&(n.value=e)}),{args:e,page:n}},template:`
      <CspPagination
        v-bind="args"
        v-model:page="page"
      />
    `})},l={name:`Par défaut`},u={name:`Cas courants`,render:s([{name:`Pagination standard`,page:5,pageCount:12,siblingCount:1,showFirstLast:!0,showDirectionLabels:!0,disabled:!1},{name:`Peu de pages`,page:1,pageCount:2,siblingCount:1,showFirstLast:!0,showDirectionLabels:!0,disabled:!1},{name:`Liste longue`,page:24,pageCount:48,siblingCount:2,showFirstLast:!0,showDirectionLabels:!0,disabled:!1}]),parameters:{controls:{disable:!0},docs:{description:{story:`Regroupe les formes les plus fréquentes de pagination pour revue rapide du comportement et du rendu.`}}}},d={name:`États et options`,render:s([{name:`Sans première et dernière page`,page:3,pageCount:8,siblingCount:1,showFirstLast:!1,showDirectionLabels:!0,disabled:!1},{name:`État désactivé`,page:5,pageCount:12,siblingCount:1,showFirstLast:!0,showDirectionLabels:!0,disabled:!0}]),parameters:{controls:{disable:!0},docs:{description:{story:`Regroupe les variantes d’état et les options d’affichage qui modifient la structure de navigation.`}}}},f={name:`Libellés de navigation`,render:s([{name:`Avec libellés`,page:5,pageCount:12,siblingCount:1,showFirstLast:!0,showDirectionLabels:!0,disabled:!1},{name:`Sans libellés`,page:5,pageCount:12,siblingCount:1,showFirstLast:!0,showDirectionLabels:!1,disabled:!1}]),parameters:{controls:{disable:!0},docs:{description:{story:`Compare la présence ou l’absence des libellés directionnels sur les boutons précédent et suivant.`}}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Cas courants',
  render: createGalleryRender([{
    name: 'Pagination standard',
    page: 5,
    pageCount: 12,
    siblingCount: 1,
    showFirstLast: true,
    showDirectionLabels: true,
    disabled: false
  }, {
    name: 'Peu de pages',
    page: 1,
    pageCount: 2,
    siblingCount: 1,
    showFirstLast: true,
    showDirectionLabels: true,
    disabled: false
  }, {
    name: 'Liste longue',
    page: 24,
    pageCount: 48,
    siblingCount: 2,
    showFirstLast: true,
    showDirectionLabels: true,
    disabled: false
  }]),
  parameters: {
    controls: {
      disable: true
    },
    docs: {
      description: {
        story: 'Regroupe les formes les plus fréquentes de pagination pour revue rapide du comportement et du rendu.'
      }
    }
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'États et options',
  render: createGalleryRender([{
    name: 'Sans première et dernière page',
    page: 3,
    pageCount: 8,
    siblingCount: 1,
    showFirstLast: false,
    showDirectionLabels: true,
    disabled: false
  }, {
    name: 'État désactivé',
    page: 5,
    pageCount: 12,
    siblingCount: 1,
    showFirstLast: true,
    showDirectionLabels: true,
    disabled: true
  }]),
  parameters: {
    controls: {
      disable: true
    },
    docs: {
      description: {
        story: 'Regroupe les variantes d’état et les options d’affichage qui modifient la structure de navigation.'
      }
    }
  }
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  name: 'Libellés de navigation',
  render: createGalleryRender([{
    name: 'Avec libellés',
    page: 5,
    pageCount: 12,
    siblingCount: 1,
    showFirstLast: true,
    showDirectionLabels: true,
    disabled: false
  }, {
    name: 'Sans libellés',
    page: 5,
    pageCount: 12,
    siblingCount: 1,
    showFirstLast: true,
    showDirectionLabels: false,
    disabled: false
  }]),
  parameters: {
    controls: {
      disable: true
    },
    docs: {
      description: {
        story: 'Compare la présence ou l’absence des libellés directionnels sur les boutons précédent et suivant.'
      }
    }
  }
}`,...f.parameters?.docs?.source}}},p=[`Playground`,`UsagePatterns`,`States`,`DirectionLabels`]}))();export{f as DirectionLabels,l as Playground,d as States,u as UsagePatterns,p as __namedExportsOrder,c as default};