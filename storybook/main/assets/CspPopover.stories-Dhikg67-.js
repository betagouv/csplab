import{n as e}from"./rolldown-runtime-sJBDdmOt.js";import{n as t,t as n}from"./CspPopover-BRfiCTui.js";import{n as r,t as i}from"./CspButton-er5uNlbR.js";import{n as a,t as o}from"./useStoryOpenState-DG0RJI2o.js";var s,c,l,u,d,f;function p(){return(p=e((()=>{r(),t(),o(),s={title:`Éléments/Génériques/CspPopover`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`open`,`side`,`align`,`padding`,`collisionPadding`]},docs:{description:{component:"Popover générique construit sur la primitive `reka-ui`. Affiche un contenu flottant ancré au déclencheur du slot `trigger`. Avec le slot `anchor`, le popover s'ancre à l'élément du slot et s'ouvre par `v-model:open`. Gère le focus, la touche Échap et le clic extérieur. Le slot par défaut reçoit le contenu libre."}},layout:`centered`},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},side:{control:{type:`radio`},options:[`top`,`right`,`bottom`,`left`],description:`Côté d'apparition du popover.`,table:{type:{summary:`top | right | bottom | left`},defaultValue:{summary:`bottom`}}},align:{control:{type:`radio`},options:[`start`,`center`,`end`],description:`Alignement du popover par rapport au déclencheur.`,table:{type:{summary:`start | center | end`},defaultValue:{summary:`start`}}},padding:{control:{type:`radio`},options:[`default`,`menu`],description:"Marge intérieure : `default` pour un contenu libre, `menu` pour une liste d'options.",table:{type:{summary:`default | menu`},defaultValue:{summary:`default`}}},collisionPadding:{control:{type:`number`},description:`Marge en pixels que le popover garde avec les bords de l'écran.`,table:{type:{summary:`number`},defaultValue:{summary:`16`}}},trigger:{control:!1,table:{disable:!0}},anchor:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{side:`bottom`,align:`start`,padding:`default`,collisionPadding:16},render:e=>({components:{CspPopover:n,CspButton:i},setup(){let{controlledOpen:t,handleUpdateOpen:n,open:r}=a(e);return{args:e,controlledOpen:t,handleUpdateOpen:n,open:r}},template:`
      <CspPopover v-bind="args" :open="controlledOpen" @update:open="handleUpdateOpen">
        <template #trigger>
          <CspButton
            :label="(open ? 'Fermer' : 'Ouvrir') + ' le popover'"
            variant="secondary"
            icon="ri:settings-3-line"
            :is-icon-left="true"
          />
        </template>

        <p class="text-sm">Contenu libre du popover.</p>
      </CspPopover>
    `})},c={name:`Par défaut`},l={name:`Côtés`,render:e=>({components:{CspPopover:n,CspButton:i},setup(){return{args:e,sides:[{label:`Haut`,value:`top`},{label:`Droite`,value:`right`},{label:`Bas`,value:`bottom`},{label:`Gauche`,value:`left`}]}},template:`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspPopover
            v-bind="args"
            :side="s.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover côté ' + s.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>

            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    `})},u={name:`Alignements`,render:e=>({components:{CspPopover:n,CspButton:i},setup(){return{args:e,alignments:[{label:`Début`,value:`start`},{label:`Centre`,value:`center`},{label:`Fin`,value:`end`}]}},template:`
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspPopover
            v-bind="args"
            :align="a.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover aligné ' + a.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>
            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    `})},d={name:`Ancré à un élément`,render:e=>({components:{CspPopover:n,CspButton:i},setup(){let{open:t,handleUpdateOpen:n}=a(e);return{args:e,open:t,handleUpdateOpen:n}},template:`
      <div class="flex gap-4 items-center">
        <CspButton label="Ouvrir le popover" variant="secondary" @click="handleUpdateOpen(true)" />
        <CspPopover v-bind="args" :open="open" @update:open="handleUpdateOpen">
          <template #anchor>
            <span class="text-sm">Élément d'ancrage</span>
          </template>
          <p class="text-sm">Contenu libre du popover.</p>
        </CspPopover>
      </div>
    `})},f=[`Default`,`Sides`,`Alignments`,`Anchored`],c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  name: 'Côtés',
  render: (args: CspPopoverProps) => ({
    components: {
      CspPopover,
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
        value: NonNullable<CspPopoverProps['side']>;
      }[];
      return {
        args,
        sides
      };
    },
    template: \`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspPopover
            v-bind="args"
            :side="s.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover côté ' + s.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>

            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    \`
  })
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Alignements',
  render: (args: CspPopoverProps) => ({
    components: {
      CspPopover,
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
        value: NonNullable<CspPopoverProps['align']>;
      }[];
      return {
        args,
        alignments
      };
    },
    template: \`
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspPopover
            v-bind="args"
            :align="a.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover aligné ' + a.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>
            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    \`
  })
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Ancré à un élément',
  render: (args: CspPopoverProps) => ({
    components: {
      CspPopover,
      CspButton
    },
    setup() {
      const {
        open,
        handleUpdateOpen
      } = useStoryOpenState(args);
      return {
        args,
        open,
        handleUpdateOpen
      };
    },
    template: \`
      <div class="flex gap-4 items-center">
        <CspButton label="Ouvrir le popover" variant="secondary" @click="handleUpdateOpen(true)" />
        <CspPopover v-bind="args" :open="open" @update:open="handleUpdateOpen">
          <template #anchor>
            <span class="text-sm">Élément d'ancrage</span>
          </template>
          <p class="text-sm">Contenu libre du popover.</p>
        </CspPopover>
      </div>
    \`
  })
}`,...d.parameters?.docs?.source}}}})))()}p();export{u as Alignments,d as Anchored,c as Default,l as Sides,f as __namedExportsOrder,s as default};