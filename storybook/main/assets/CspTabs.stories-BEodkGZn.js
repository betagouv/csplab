import{i as e}from"./preload-helper-Ct_ODC0V.js";import{At as t,D as n,gt as r}from"./iframe-z3OQyoHs.js";import{a as i,i as a,n as o,o as s,r as c,t as l}from"./CspTabs-hzr1aAv-.js";var u,d,f,p,m,h,g,_;e((()=>{n(),o(),s(),a(),u={title:`Éléments/Génériques/CspTabs`,component:l,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`tabs`,`defaultValue`,`orientation`,`activationMode`]},docs:{description:{component:"Composant d'onglets accessible basé sur Reka UI. Usage monolithique : passez `tabs` et fournissez un slot nommé par valeur d'onglet. Usage composé : placez `CspTabsList` et `CspTabsPanels` dans le slot par défaut pour répartir la barre et les panneaux dans des régions de layout différentes (p. ex. la barre dans un en-tête de page)."}}},argTypes:{modelValue:{control:{type:`text`},description:`Onglet actuellement actif (v-model).`,table:{type:{summary:`string`}}},tabs:{control:{type:`object`},description:`Liste des onglets disponibles.`,table:{type:{summary:`{ value: string; label: string; icon?: string; disabled?: boolean }[]`}}},defaultValue:{control:{type:`text`},description:`Valeur de l'onglet actif par défaut (non contrôlé).`,table:{type:{summary:`string`}}},orientation:{control:{type:`radio`},options:[`horizontal`,`vertical`],description:`Orientation des onglets.`,table:{type:{summary:`'horizontal' | 'vertical'`},defaultValue:{summary:`'horizontal'`}}},activationMode:{control:{type:`radio`},options:[`automatic`,`manual`],description:`Mode d'activation : automatique au focus ou manuel au clic.`,table:{type:{summary:`'automatic' | 'manual'`},defaultValue:{summary:`'automatic'`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{tabs:[{value:`tab-1`,label:`Onglet 1`},{value:`tab-2`,label:`Onglet 2`},{value:`tab-3`,label:`Onglet 3`}],defaultValue:`tab-1`,orientation:`horizontal`,activationMode:`automatic`},render:e=>({components:{CspTabs:l},setup(){let n=t(e.modelValue??e.defaultValue??``);return r(()=>e.modelValue,e=>{e!==void 0&&(n.value=e)}),{args:e,selected:n}},template:`
      <CspTabs
        v-bind="args"
        v-model="selected"
      >
        <template #tab-1>
          <p>Contenu du premier onglet.</p>
        </template>
        <template #tab-2>
          <p>Contenu du deuxième onglet.</p>
        </template>
        <template #tab-3>
          <p>Contenu du troisième onglet.</p>
        </template>
      </CspTabs>
    `})},d={name:`Usage monolithique`},f={name:`Usage composé`,parameters:{docs:{description:{story:`Usage composé : la barre (CspTabsList) et les panneaux (CspTabsPanels) sont rendus séparément tout en partageant l’état, ici la barre dans un en-tête simulé et les panneaux en dessous.`}}},render:e=>({components:{CspTabs:l,CspTabsList:i,CspTabsPanels:c},setup(){return{args:e,selected:t(e.defaultValue??`tab-1`)}},template:`
      <CspTabs v-model="selected" :default-value="args.defaultValue">
        <div style="border:1px solid var(--border-default-grey);padding:1rem;margin-bottom:1rem">
          <strong>En-tête de page</strong>
          <CspTabsList :tabs="args.tabs" />
        </div>
        <CspTabsPanels :tabs="args.tabs">
          <template #tab-1><p>Contenu du premier onglet.</p></template>
          <template #tab-2><p>Contenu du deuxième onglet.</p></template>
          <template #tab-3><p>Contenu du troisième onglet.</p></template>
        </CspTabsPanels>
      </CspTabs>
    `})},p={name:`Avec onglet désactivé`,args:{tabs:[{value:`tab-1`,label:`Onglet 1`},{value:`tab-2`,label:`Onglet 2`,disabled:!0},{value:`tab-3`,label:`Onglet 3`}],defaultValue:`tab-1`}},m={name:`Orientation verticale`,args:{orientation:`vertical`}},h={name:`Activation manuelle`,args:{activationMode:`manual`},parameters:{docs:{description:{story:`En mode manuel, les onglets ne s'activent qu'au clic et non au focus clavier.`}}}},g={name:`Avec icônes`,args:{tabs:[{value:`tab-1`,label:`Accueil`,icon:`ri:home-line`},{value:`tab-2`,label:`Paramètres`,icon:`ri:settings-3-line`},{value:`tab-3`,label:`Utilisateurs`,icon:`ri:user-line`}],defaultValue:`tab-1`}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Usage monolithique'
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  name: 'Usage composé',
  parameters: {
    docs: {
      description: {
        story: 'Usage composé : la barre (CspTabsList) et les panneaux (CspTabsPanels) sont rendus séparément tout en partageant l’état, ici la barre dans un en-tête simulé et les panneaux en dessous.'
      }
    }
  },
  render: (args: CspTabsProps) => ({
    components: {
      CspTabs,
      CspTabsList,
      CspTabsPanels
    },
    setup() {
      const selected = ref(args.defaultValue ?? 'tab-1');
      return {
        args,
        selected
      };
    },
    template: \`
      <CspTabs v-model="selected" :default-value="args.defaultValue">
        <div style="border:1px solid var(--border-default-grey);padding:1rem;margin-bottom:1rem">
          <strong>En-tête de page</strong>
          <CspTabsList :tabs="args.tabs" />
        </div>
        <CspTabsPanels :tabs="args.tabs">
          <template #tab-1><p>Contenu du premier onglet.</p></template>
          <template #tab-2><p>Contenu du deuxième onglet.</p></template>
          <template #tab-3><p>Contenu du troisième onglet.</p></template>
        </CspTabsPanels>
      </CspTabs>
    \`
  })
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  name: 'Avec onglet désactivé',
  args: {
    tabs: [{
      value: 'tab-1',
      label: 'Onglet 1'
    }, {
      value: 'tab-2',
      label: 'Onglet 2',
      disabled: true
    }, {
      value: 'tab-3',
      label: 'Onglet 3'
    }],
    defaultValue: 'tab-1'
  }
}`,...p.parameters?.docs?.source}}},m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  name: 'Orientation verticale',
  args: {
    orientation: 'vertical'
  }
}`,...m.parameters?.docs?.source}}},h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{
  name: 'Activation manuelle',
  args: {
    activationMode: 'manual'
  },
  parameters: {
    docs: {
      description: {
        story: 'En mode manuel, les onglets ne s\\'activent qu\\'au clic et non au focus clavier.'
      }
    }
  }
}`,...h.parameters?.docs?.source}}},g.parameters={...g.parameters,docs:{...g.parameters?.docs,source:{originalSource:`{
  name: 'Avec icônes',
  args: {
    tabs: [{
      value: 'tab-1',
      label: 'Accueil',
      icon: 'ri:home-line'
    }, {
      value: 'tab-2',
      label: 'Paramètres',
      icon: 'ri:settings-3-line'
    }, {
      value: 'tab-3',
      label: 'Utilisateurs',
      icon: 'ri:user-line'
    }],
    defaultValue: 'tab-1'
  }
}`,...g.parameters?.docs?.source}}},_=[`Default`,`Composed`,`WithDisabledTab`,`Vertical`,`ManualActivation`,`WithIcons`]}))();export{f as Composed,d as Default,h as ManualActivation,m as Vertical,p as WithDisabledTab,g as WithIcons,_ as __namedExportsOrder,u as default};