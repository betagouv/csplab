import{i as e}from"./preload-helper-DVWsqyFp.js";import{$ as t,B as n,D as r,G as i,K as a,Lt as o,V as s,ht as c,lt as l,mt as u,ot as d,yt as f}from"./iframe-Cav10qEp.js";import{Qt as p,Xt as m,en as h,nn as g,t as _}from"./dist-DJiDhsDT.js";import{n as v,t as y}from"./CspButton-C1ocScaJ.js";import{n as b,t as x}from"./useStoryOpenState-CtqobOzh.js";var S,C=e((()=>{r(),_(),S=a({inheritAttrs:!1,__name:`CspPopover`,props:t({side:{default:`bottom`},align:{default:`start`}},{open:{type:Boolean},openModifiers:{}}),emits:[`update:open`],setup(e){let t=u(e,`open`),r=!!c().trigger;return(a,c)=>(d(),n(o(g),{open:t.value,"onUpdate:open":c[0]||=e=>t.value=e},{default:f(()=>[o(r)?(d(),n(o(m),{key:0,"as-child":``},{default:f(()=>[l(a.$slots,`trigger`)]),_:3})):s(``,!0),i(o(p),null,{default:f(()=>[i(o(h),{class:`csp-popover`,side:e.side,align:e.align,"side-offset":6},{default:f(()=>[l(a.$slots,`default`)]),_:3},8,[`side`,`align`])]),_:3})]),_:3},8,[`open`]))}})})),w=e((()=>{})),T,E=e((()=>{C(),C(),w(),T=S,S.__docgenInfo=Object.assign({displayName:S.name??S.__name},{exportName:`default`,displayName:`CspPopover`,type:1,props:[{name:`side`,global:!1,description:``,tags:[],required:!1,type:`"right" | "left" | "top" | "bottom"`,declarations:[],schema:{kind:`enum`,type:`"right" | "left" | "top" | "bottom"`,schema:[`"right"`,`"left"`,`"top"`,`"bottom"`]},default:`"bottom"`},{name:`align`,global:!1,description:``,tags:[],required:!1,type:`"start" | "center" | "end"`,declarations:[],schema:{kind:`enum`,type:`"start" | "center" | "end"`,schema:[`"start"`,`"center"`,`"end"`]},default:`"start"`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`open`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],events:[{name:`update:open`,description:``,tags:[],type:`[value: boolean]`,signature:`(event: "update:open", value: boolean): void`,declarations:[],schema:[{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}]}],slots:[{name:`trigger`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`side`,type:`"right" | "left" | "top" | "bottom"`,description:``,declarations:[],schema:{kind:`enum`,type:`"right" | "left" | "top" | "bottom"`,schema:[`"right"`,`"left"`,`"top"`,`"bottom"`]}},{name:`align`,type:`"start" | "center" | "end"`,description:``,declarations:[],schema:{kind:`enum`,type:`"start" | "center" | "end"`,schema:[`"start"`,`"center"`,`"end"`]}},{name:`open`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspPopover/CspPopover.vue`})})),D,O,k,A,j;e((()=>{v(),E(),x(),D={title:`Éléments/Génériques/CspPopover`,component:T,tags:[`autodocs`],parameters:{controls:{include:[`open`,`side`,`align`]},docs:{description:{component:"Popover générique construit sur la primitive `reka-ui`. Affiche un contenu flottant ancré à un déclencheur via le slot `trigger`. Gère le focus, la touche Échap et le clic extérieur. Le slot par défaut reçoit le contenu libre."}},layout:`centered`},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},side:{control:{type:`radio`},options:[`top`,`right`,`bottom`,`left`],description:`Côté d'apparition du popover.`,table:{type:{summary:`top | right | bottom | left`},defaultValue:{summary:`bottom`}}},align:{control:{type:`radio`},options:[`start`,`center`,`end`],description:`Alignement du popover par rapport au déclencheur.`,table:{type:{summary:`start | center | end`},defaultValue:{summary:`start`}}},trigger:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{side:`bottom`,align:`start`},render:e=>({components:{CspPopover:T,CspButton:y},setup(){let{controlledOpen:t,handleUpdateOpen:n,open:r}=b(e);return{args:e,controlledOpen:t,handleUpdateOpen:n,open:r}},template:`
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
    `})},O={name:`Par défaut`},k={name:`Côtés`,render:e=>({components:{CspPopover:T,CspButton:y},setup(){return{args:e,sides:[{label:`Haut`,value:`top`},{label:`Droite`,value:`right`},{label:`Bas`,value:`bottom`},{label:`Gauche`,value:`left`}]}},template:`
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
    `})},A={name:`Alignements`,render:e=>({components:{CspPopover:T,CspButton:y},setup(){return{args:e,alignments:[{label:`Début`,value:`start`},{label:`Centre`,value:`center`},{label:`Fin`,value:`end`}]}},template:`
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
    `})},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...O.parameters?.docs?.source}}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{
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
}`,...k.parameters?.docs?.source}}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`{
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
}`,...A.parameters?.docs?.source}}},j=[`Default`,`Sides`,`Alignments`]}))();export{A as Alignments,O as Default,k as Sides,j as __namedExportsOrder,D as default};