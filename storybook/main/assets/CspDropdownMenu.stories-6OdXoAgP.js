import{i as e}from"./preload-helper-Ct_ODC0V.js";import{n as t,t as n}from"./CspButton-BGobc-vp.js";import{n as r,t as i}from"./CspDropdownMenu-CyPadj77.js";import{n as a,t as o}from"./useStoryOpenState-DeV4tdSb.js";var s,c,l,u,d;e((()=>{t(),r(),o(),s={title:`Éléments/Génériques/CspDropdownMenu`,component:i,tags:[`autodocs`],parameters:{controls:{include:[`open`,`align`,`side`,`sideOffset`]},docs:{description:{component:"Menu déroulant accessible basé sur les primitives `reka-ui`. Utilisez le slot `trigger` pour l'élément déclencheur et le slot par défaut pour les items du menu."}}},argTypes:{sections:{control:!1,description:"Sections d'items. Chaque section peut contenir plusieurs `{ label, icon?, disabled?, destructive?, onSelect? }`.",table:{type:{summary:`CspDropdownMenuSection[]`}}},open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},align:{control:{type:`radio`},options:[`start`,`center`,`end`],description:`Alignement du menu par rapport au déclencheur.`,table:{type:{summary:`start | center | end`},defaultValue:{summary:`start`}}},side:{control:{type:`radio`},options:[`top`,`right`,`bottom`,`left`],description:`Position du menu par rapport au déclencheur.`,table:{type:{summary:`top | right | bottom | left`},defaultValue:{summary:`top`}}},sideOffset:{control:{type:`number`},description:`Distance entre le menu et le déclencheur, en pixels.`,table:{type:{summary:`number`},defaultValue:{summary:`8`}}},trigger:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{sections:[{items:[{label:`Ouvrir`,icon:`ri:external-link-line`},{label:`Renommer`,icon:`ri:pencil-line`}]},{items:[{label:`Dupliquer`,icon:`ri:file-copy-line`,disabled:!0},{label:`Supprimer`,icon:`ri:delete-bin-line`,destructive:!0}]}],align:`start`,side:`bottom`,sideOffset:8},render:e=>({components:{CspDropdownMenu:i,CspButton:n},setup(){let{controlledOpen:t,handleUpdateOpen:n}=a(e);return{args:e,controlledOpen:t,handleUpdateOpen:n}},template:`
      <CspDropdownMenu
        v-bind="args"
        :open="controlledOpen"
        @update:open="handleUpdateOpen"
      >
        <template #trigger>
          <CspButton
            icon="ri:more-2-line"
            variant="tertiary"
            label="Ouvrir le menu déroulant"
          />
        </template>
      </CspDropdownMenu>
    `})},c={name:`Par défaut`},l={name:`Côtés`,render:e=>({components:{CspDropdownMenu:i,CspButton:n},setup(){return{sides:[{label:`Haut`,value:`top`},{label:`Droite`,value:`right`},{label:`Bas`,value:`bottom`},{label:`Gauche`,value:`left`}],args:e}},template:`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspDropdownMenu
            v-bind="args"
            :key="s.value"
            :side="s.value"
          >
            <template #trigger>
              <CspButton :label="s.label" variant="tertiary" />
            </template>
            <p class="text-sm">Contenu libre du menu déroulant.</p>
          </CspDropdownMenu>
        </div>
      </div>
    `})},u={name:`Alignements`,render:e=>({components:{CspDropdownMenu:i,CspButton:n},setup(){return{alignments:[{label:`Début`,value:`start`},{label:`Centre`,value:`center`},{label:`Fin`,value:`end`}],args:e}},template:`
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspDropdownMenu
            v-bind="args"
            :key="a.value"
            :align="a.value"
          >
            <template #trigger>
              <CspButton :label="a.label" variant="tertiary" />
            </template>
            <p class="text-sm">Contenu libre du menu déroulant.</p>
          </CspDropdownMenu>
        </div>
      </div>
    `})},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  name: 'Côtés',
  render: (args: CspDropdownMenuProps) => ({
    components: {
      CspDropdownMenu,
      CspButton
    },
    setup() {
      const sides = [{
        label: 'Haut',
        value: 'top'
      }, {
        label: 'Droite',
        value: 'right'
      }, {
        label: 'Bas',
        value: 'bottom'
      }, {
        label: 'Gauche',
        value: 'left'
      }] satisfies {
        label: string;
        value: NonNullable<CspDropdownMenuProps['side']>;
      }[];
      return {
        sides,
        args
      };
    },
    template: \`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspDropdownMenu
            v-bind="args"
            :key="s.value"
            :side="s.value"
          >
            <template #trigger>
              <CspButton :label="s.label" variant="tertiary" />
            </template>
            <p class="text-sm">Contenu libre du menu déroulant.</p>
          </CspDropdownMenu>
        </div>
      </div>
    \`
  })
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Alignements',
  render: (args: CspDropdownMenuProps) => ({
    components: {
      CspDropdownMenu,
      CspButton
    },
    setup() {
      const alignments = [{
        label: 'Début',
        value: 'start'
      }, {
        label: 'Centre',
        value: 'center'
      }, {
        label: 'Fin',
        value: 'end'
      }] satisfies {
        label: string;
        value: NonNullable<CspDropdownMenuProps['align']>;
      }[];
      return {
        alignments,
        args
      };
    },
    template: \`
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspDropdownMenu
            v-bind="args"
            :key="a.value"
            :align="a.value"
          >
            <template #trigger>
              <CspButton :label="a.label" variant="tertiary" />
            </template>
            <p class="text-sm">Contenu libre du menu déroulant.</p>
          </CspDropdownMenu>
        </div>
      </div>
    \`
  })
}`,...u.parameters?.docs?.source}}},d=[`Default`,`Sides`,`Alignments`]}))();export{u as Alignments,c as Default,l as Sides,d as __namedExportsOrder,s as default};