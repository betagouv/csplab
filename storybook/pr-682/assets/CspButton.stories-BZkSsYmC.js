import{j as A,e as P,U as D,r as E,M as T,a as O,x as p,g as d,I as Z,f as u,i as $}from"./vue.esm-bundler-r3PfzcfG.js";import{P as K}from"./Primitive-DB9Ahhg1.js";import{_ as j}from"./CspIcon-Dxv71jIS.js";import{_ as F}from"./_plugin-vue_export-helper-DlAUqK2U.js";const G={key:0,class:"csp-btn__label"},M={key:1,class:"btn__icon"},N=A({__name:"CspButton",props:{asChild:{type:Boolean},as:{default:"button"},variant:{default:"primary"},size:{default:"md"},isIconLeft:{type:Boolean,default:!1},label:{},icon:{}},setup(e){const s=e,c=O(()=>!!s.icon&&!s.label);return(U,H)=>(p(),P(T(K),E(s,{class:["csp-btn",[`csp-btn--${e.variant}`,`csp-btn--${e.size}`,{"csp-btn--icon-only":c.value},{"csp-btn--icon-left":!c.value&&e.isIconLeft&&!!e.icon},{"csp-btn--icon-right":!c.value&&!e.isIconLeft&&!!e.icon}]]}),{default:D(()=>[e.label?(p(),d("span",G,Z(e.label),1)):u("",!0),e.icon?(p(),d("span",M,[$(j,{class:"csp-btn__icon",name:e.icon},null,8,["name"])])):u("",!0)]),_:1},16,["class"]))}}),n=F(N,[["__scopeId","data-v-aa4cac9c"]]);N.__docgenInfo={exportName:"default",displayName:"CspButton",type:1,props:[{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"}],events:[],slots:[],exposed:[],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspButton/CspButton.vue"};const Y={title:"Éléments/Génériques/CspButton",component:n,tags:["autodocs"],parameters:{controls:{include:["variant","size","isIconLeft","label","icon","as","asChild"]},docs:{description:{component:"Bouton générique. Doit avoir un `label`, une `icon`, ou les deux."}}},argTypes:{variant:{control:{type:"radio"},options:["primary","secondary","tertiary","tertiary-no-outline"],description:"Style visuel.",table:{type:{summary:"primary | secondary | tertiary | tertiary-no-outline"},defaultValue:{summary:"primary"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille du bouton.",table:{type:{summary:"sm | md | lg"},defaultValue:{summary:"md"}}},isIconLeft:{control:{type:"boolean"},description:"Afficher l'icône avant le libellé.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},label:{control:{type:"text"},description:"Texte du bouton. Requis si `icon` est absent.",table:{type:{summary:"string"}}},icon:{control:{type:"text"},description:"Nom Iconify. Requis si `label` est absent.",table:{type:{summary:"string"}}},as:{control:{type:"text"},description:"Élément ou composant rendu.",table:{type:{summary:"string | Component"},defaultValue:{summary:"button"}}},asChild:{control:{type:"boolean"},description:"Rendre l'enfant comme élément racine.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:"primary",size:"md",isIconLeft:!1,label:"Libellé du bouton",asChild:!1},render:e=>({components:{CspButton:n},setup(){return{args:e}},template:'<CspButton v-bind="args" />'})},q=["primary","secondary","tertiary","tertiary-no-outline"],R=["sm","md","lg"],a={args:{label:"Button label"}},t={render:e=>({components:{CspButton:n},setup(){return{variants:q,args:e}},template:`
      <div class="flex flex-row gap-12">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <CspButton
            v-bind="args"
            :variant="v"
            label="Label"
          />
        </div>
      </div>
    `})},r={render:e=>({components:{CspButton:n},setup(){return{sizes:R,args:e}},template:`
      <div class="flex flex-row gap-12">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <CspButton
            v-bind="args"
            :size="s"
            label="Label"
          />
        </div>
      </div>
    `})},o={render:e=>({components:{CspButton:n},setup(){return{args:e,iconVariants:[{description:"No icon",props:{label:"Label"}},{description:"Icon right",props:{label:"Label",icon:"ri:arrow-right-line"}},{description:"Icon left",props:{label:"Label",icon:"ri:arrow-left-line",isIconLeft:!0}},{description:"Icon only",props:{icon:"ri:checkbox-circle-line",label:void 0}}],sizes:R}},template:`
      <div class="flex flex-col gap-12">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p>{{ s }}</p>
          <div class="flex flex-row gap-12">
            <div
              v-for="v in iconVariants"
              :key="v.description"
            >
              <p class="mb-2">{{ v.description }}</p>
              <CspButton
                v-bind="{ ...args, ...v.props }"
                :size="s"
              />
            </div>
          </div>
        </div>
      </div>
    `})},i={render:e=>({components:{CspButton:n},setup(){return{variants:q,args:e}},template:`
      <div class="flex flex-col gap-3">
        <div
          v-for="v in variants"
          :key="v"
          class="flex gap-3 items-center"
        >
          <p class="w-24">{{ v }}</p>
          <CspButton
            :variant="v"
            v-bind="args"
            label="Default"
          />
          <CspButton
            :variant="v"
            v-bind="args"
            :disabled="true"
            label="Disabled"
          />
        </div>
      </div>
    `})},l={render:()=>({components:{CspButton:n},template:`
      <CspButton
        as="a"
        href="https://www.csplab.beta.gouv.fr"
        target="_blank"
        label="Visit CSPLab"
        icon="ri:external-link-line"
      />
    `})};var m,b,v;a.parameters={...a.parameters,docs:{...(m=a.parameters)==null?void 0:m.docs,source:{originalSource:`{
  args: {
    label: 'Button label'
  }
}`,...(v=(b=a.parameters)==null?void 0:b.docs)==null?void 0:v.source}}};var f,y,g;t.parameters={...t.parameters,docs:{...(f=t.parameters)==null?void 0:f.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspButton
    },
    setup() {
      return {
        variants: VARIANTS,
        args
      };
    },
    template: \`
      <div class="flex flex-row gap-12">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <CspButton
            v-bind="args"
            :variant="v"
            label="Label"
          />
        </div>
      </div>
    \`
  })
}`,...(g=(y=t.parameters)==null?void 0:y.docs)==null?void 0:g.source}}};var x,C,k;r.parameters={...r.parameters,docs:{...(x=r.parameters)==null?void 0:x.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspButton
    },
    setup() {
      return {
        sizes: SIZES,
        args
      };
    },
    template: \`
      <div class="flex flex-row gap-12">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <CspButton
            v-bind="args"
            :size="s"
            label="Label"
          />
        </div>
      </div>
    \`
  })
}`,...(k=(C=r.parameters)==null?void 0:C.docs)==null?void 0:k.source}}};var B,h,I;o.parameters={...o.parameters,docs:{...(B=o.parameters)==null?void 0:B.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspButton
    },
    setup() {
      const iconVariants = [{
        description: 'No icon',
        props: {
          label: 'Label'
        }
      }, {
        description: 'Icon right',
        props: {
          label: 'Label',
          icon: 'ri:arrow-right-line'
        }
      }, {
        description: 'Icon left',
        props: {
          label: 'Label',
          icon: 'ri:arrow-left-line',
          isIconLeft: true
        }
      }, {
        description: 'Icon only',
        props: {
          icon: 'ri:checkbox-circle-line',
          label: undefined
        }
      }] as const;
      return {
        args,
        iconVariants,
        sizes: SIZES
      };
    },
    template: \`
      <div class="flex flex-col gap-12">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p>{{ s }}</p>
          <div class="flex flex-row gap-12">
            <div
              v-for="v in iconVariants"
              :key="v.description"
            >
              <p class="mb-2">{{ v.description }}</p>
              <CspButton
                v-bind="{ ...args, ...v.props }"
                :size="s"
              />
            </div>
          </div>
        </div>
      </div>
    \`
  })
}`,...(I=(h=o.parameters)==null?void 0:h.docs)==null?void 0:I.source}}};var w,L,S;i.parameters={...i.parameters,docs:{...(w=i.parameters)==null?void 0:w.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspButton
    },
    setup() {
      return {
        variants: VARIANTS,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-3">
        <div
          v-for="v in variants"
          :key="v"
          class="flex gap-3 items-center"
        >
          <p class="w-24">{{ v }}</p>
          <CspButton
            :variant="v"
            v-bind="args"
            label="Default"
          />
          <CspButton
            :variant="v"
            v-bind="args"
            :disabled="true"
            label="Disabled"
          />
        </div>
      </div>
    \`
  })
}`,...(S=(L=i.parameters)==null?void 0:L.docs)==null?void 0:S.source}}};var V,z,_;l.parameters={...l.parameters,docs:{...(V=l.parameters)==null?void 0:V.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspButton
    },
    template: \`
      <CspButton
        as="a"
        href="https://www.csplab.beta.gouv.fr"
        target="_blank"
        label="Visit CSPLab"
        icon="ri:external-link-line"
      />
    \`
  })
}`,...(_=(z=l.parameters)==null?void 0:z.docs)==null?void 0:_.source}}};const ee=["Default","Variants","Sizes","Icons","States","AsLink"];export{l as AsLink,a as Default,o as Icons,r as Sizes,i as States,t as Variants,ee as __namedExportsOrder,Y as default};
