import{C as n}from"./CspButton-DdZRQonE.js";import{_ as s}from"./CspDropdownMenu-Bq5MaDSR.js";import{u as f}from"./useStoryOpenState-Dt1ghQp-.js";import"./vue.esm-bundler-7zVN4DZj.js";import"./Primitive-DzgJnGz8.js";import"./CspIcon-ClPxlQGO.js";import"./iconify-DRloO12f.js";import"./_plugin-vue_export-helper-DlAUqK2U.js";import"./useForwardExpose-qwf_wVRM.js";import"./Collection-C9Lj7FBv.js";import"./ConfigProvider-lmrMonQJ.js";import"./usePrimitiveElement-BQ6g5-es.js";import"./PopperContent-DMAzS00b.js";import"./Teleport-D2JxKccQ.js";import"./nullish-CHIgUVhi.js";import"./handleAndDispatchCustomEvent-ChOKVcqp.js";import"./useId-Blg3GNwK.js";import"./Presence-CGGvXRHO.js";import"./FocusScope-kJbVssvv.js";import"./useFocusGuards-lofhKZlc.js";import"./useTypeahead-D036ReqY.js";import"./utils-DkPExA7K.js";import"./RovingFocusGroup-DzvvbqBY.js";const y=[{items:[{label:"Ouvrir",icon:"ri:external-link-line"},{label:"Renommer",icon:"ri:pencil-line"}]},{items:[{label:"Dupliquer",icon:"ri:file-copy-line",disabled:!0},{label:"Supprimer",icon:"ri:delete-bin-line",destructive:!0}]}],T={title:"Éléments/Génériques/CspDropdownMenu",component:s,tags:["autodocs"],parameters:{controls:{include:["open","align","side","sideOffset"]},docs:{description:{component:"Menu déroulant accessible basé sur les primitives `reka-ui`. Utilisez le slot `trigger` pour l'élément déclencheur et le slot par défaut pour les items du menu."}}},argTypes:{sections:{control:!1,description:"Sections d'items. Chaque section peut contenir plusieurs `{ label, icon?, disabled?, destructive?, onSelect? }`.",table:{type:{summary:"CspDropdownMenuSection[]"}}},open:{control:{type:"boolean"},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:"boolean"}}},align:{control:{type:"radio"},options:["start","center","end"],description:"Alignement du menu par rapport au déclencheur.",table:{type:{summary:"start | center | end"},defaultValue:{summary:"start"}}},side:{control:{type:"radio"},options:["top","right","bottom","left"],description:"Position du menu par rapport au déclencheur.",table:{type:{summary:"top | right | bottom | left"},defaultValue:{summary:"top"}}},sideOffset:{control:{type:"number"},description:"Distance entre le menu et le déclencheur, en pixels.",table:{type:{summary:"number"},defaultValue:{summary:"8"}}},trigger:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{sections:y,align:"start",side:"bottom",sideOffset:8},render:e=>({components:{CspDropdownMenu:s,CspButton:n},setup(){const{controlledOpen:l,handleUpdateOpen:v}=f(e);return{args:e,controlledOpen:l,handleUpdateOpen:v}},template:`
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
    `})},t={name:"Par défaut"},r={name:"Côtés",render:e=>({components:{CspDropdownMenu:s,CspButton:n},setup(){return{sides:[{label:"Haut",value:"top"},{label:"Droite",value:"right"},{label:"Bas",value:"bottom"},{label:"Gauche",value:"left"}],args:e}},template:`
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
    `})},a={name:"Alignements",render:e=>({components:{CspDropdownMenu:s,CspButton:n},setup(){return{alignments:[{label:"Début",value:"start"},{label:"Centre",value:"center"},{label:"Fin",value:"end"}],args:e}},template:`
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
    `})};var o,i,p;t.parameters={...t.parameters,docs:{...(o=t.parameters)==null?void 0:o.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...(p=(i=t.parameters)==null?void 0:i.docs)==null?void 0:p.source}}};var u,d,m;r.parameters={...r.parameters,docs:{...(u=r.parameters)==null?void 0:u.docs,source:{originalSource:`{
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
}`,...(m=(d=r.parameters)==null?void 0:d.docs)==null?void 0:m.source}}};var c,b,g;a.parameters={...a.parameters,docs:{...(c=a.parameters)==null?void 0:c.docs,source:{originalSource:`{
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
}`,...(g=(b=a.parameters)==null?void 0:b.docs)==null?void 0:g.source}}};const I=["Default","Sides","Alignments"];export{a as Alignments,t as Default,r as Sides,I as __namedExportsOrder,T as default};
