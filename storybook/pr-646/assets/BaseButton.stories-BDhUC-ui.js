import{F as j,h as b,C as M,m as O,c as H,i as m,d as J,x as Q,a as U,q as f,z as W,f as g,w as X,e as B,g as Y}from"./vue.esm-bundler-D28085mC.js";import{_ as ee}from"./BaseIcon-CaSerw_D.js";function T(e){return e?e.flatMap(n=>n.type===j?T(n.children):[n]):[]}const ne=b({name:"PrimitiveSlot",inheritAttrs:!1,setup(e,{attrs:n,slots:a}){return()=>{var y;if(!a.default)return null;const t=T(a.default()),r=t.findIndex(K=>K.type!==M);if(r===-1)return t;const o=t[r];(y=o.props)==null||delete y.ref;const $=o.props?O(n,o.props):n,v=H({...o,props:{}},$);return t.length===1?v:(t[r]=v,t)}}}),te=["area","img","input"],ae=b({name:"Primitive",inheritAttrs:!1,props:{asChild:{type:Boolean,default:!1},as:{type:[String,Object],default:"div"}},setup(e,{attrs:n,slots:a}){const t=e.asChild?"template":e.as;return typeof t=="string"&&te.includes(t)?()=>m(t,n):t!=="template"?()=>m(e.as,n,{default:a.default}):()=>m(ne,n,{default:a.default})}}),se={key:0,class:"btn__label"},re={key:1,class:"btn__icon"},F=b({__name:"BaseButton",props:{asChild:{type:Boolean},as:{default:"button"},variant:{default:"primary"},size:{default:"md"},isIconLeft:{type:Boolean,default:!1},label:{},icon:{}},setup(e){const n=e,a=U(()=>!!n.icon&&!n.label);return(t,r)=>(f(),J(Q(ae),O(n,{class:["btn",[`btn--${e.variant}`,`btn--${e.size}`,{"btn--icon-only":a.value},{"btn--icon-left":!a.value&&e.isIconLeft&&!!e.icon},{"btn--icon-right":!a.value&&!e.isIconLeft&&!!e.icon}]]}),{default:W(()=>[e.label?(f(),g("span",se,X(e.label),1)):B("",!0),e.icon?(f(),g("span",re,[Y(ee,{name:e.icon},null,8,["name"])])):B("",!0)]),_:1},16,["class"]))}}),oe=(e,n)=>{const a=e.__vccOpts||e;for(const[t,r]of n)a[t]=r;return a},s=oe(F,[["__scopeId","data-v-134ea842"]]);F.__docgenInfo={exportName:"default",displayName:"BaseButton",type:1,props:[{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"}],events:[],slots:[],exposed:[],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/BaseButton/BaseButton.vue"};const ce={title:"02 - Elements/Generic/BaseButton",component:s,tags:["autodocs"],parameters:{controls:{include:["variant","size","isIconLeft","label","icon","as","asChild"]},docs:{description:{component:"Generic button. Either have a `label` or an `icon` or both."}}},argTypes:{variant:{control:{type:"radio"},options:["primary","secondary","tertiary","tertiary-no-outline"],description:"Visual style.",table:{type:{summary:"primary | secondary | tertiary | tertiary-no-outline"},defaultValue:{summary:"primary"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Button size.",table:{type:{summary:"sm | md | lg"},defaultValue:{summary:"md"}}},isIconLeft:{control:{type:"boolean"},description:"Show icon before label.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},label:{control:{type:"text"},description:"Button text. Required if `icon` is missing.",table:{type:{summary:"string"}}},icon:{control:{type:"text"},description:"Iconify name. Required if `label` is missing.",table:{type:{summary:"string"}}},as:{control:{type:"text"},description:"Rendered element or component.",table:{type:{summary:"string | Component"},defaultValue:{summary:"button"}}},asChild:{control:{type:"boolean"},description:"Render the child as the root element.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:"primary",size:"md",isIconLeft:!1,label:"Button label",asChild:!1},render:e=>({components:{BaseButton:s},setup(){return{args:e}},template:'<BaseButton v-bind="args" />'})},G=["primary","secondary","tertiary","tertiary-no-outline"],Z=["sm","md","lg"],i={args:{label:"Button label"}},l={render:e=>({components:{BaseButton:s},setup(){return{variants:G,args:e}},template:`
      <div class="flex flex-row gap-12">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <BaseButton
            v-bind="args"
            :variant="v"
            label="Label"
          />
        </div>
      </div>
    `})},c={render:e=>({components:{BaseButton:s},setup(){return{sizes:Z,args:e}},template:`
      <div class="flex flex-row gap-12">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <BaseButton
            v-bind="args"
            :size="s"
            label="Label"
          />
        </div>
      </div>
    `})},d={render:e=>({components:{BaseButton:s},setup(){return{args:e,iconVariants:[{description:"No icon",props:{label:"Label"}},{description:"Icon right",props:{label:"Label",icon:"ri:arrow-right-line"}},{description:"Icon left",props:{label:"Label",icon:"ri:arrow-left-line",isIconLeft:!0}},{description:"Icon only",props:{icon:"ri:checkbox-circle-line",label:void 0}}],sizes:Z}},template:`
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
              <BaseButton
                v-bind="{ ...args, ...v.props }"
                :size="s"
              />
            </div>
          </div>
        </div>
      </div>
    `})},p={render:e=>({components:{BaseButton:s},setup(){return{variants:G,args:e}},template:`
      <div class="flex flex-col gap-3">
        <div
          v-for="v in variants"
          :key="v"
          class="flex gap-3 items-center"
        >
          <p class="w-24">{{ v }}</p>
          <BaseButton
            :variant="v"
            v-bind="args"
            label="Default"
          />
          <BaseButton
            :variant="v"
            v-bind="args"
            :disabled="true"
            label="Disabled"
          />
        </div>
      </div>
    `})},u={render:()=>({components:{BaseButton:s},template:`
      <BaseButton
        as="a"
        href="https://www.csplab.beta.gouv.fr"
        target="_blank"
        label="Visit CSPLab"
        icon="ri:external-link-line"
      />
    `})};var h,x,k;i.parameters={...i.parameters,docs:{...(h=i.parameters)==null?void 0:h.docs,source:{originalSource:`{
  args: {
    label: 'Button label'
  }
}`,...(k=(x=i.parameters)==null?void 0:x.docs)==null?void 0:k.source}}};var I,S,w;l.parameters={...l.parameters,docs:{...(I=l.parameters)==null?void 0:I.docs,source:{originalSource:`{
  render: args => ({
    components: {
      BaseButton
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
          <BaseButton
            v-bind="args"
            :variant="v"
            label="Label"
          />
        </div>
      </div>
    \`
  })
}`,...(w=(S=l.parameters)==null?void 0:S.docs)==null?void 0:w.source}}};var L,V,C;c.parameters={...c.parameters,docs:{...(L=c.parameters)==null?void 0:L.docs,source:{originalSource:`{
  render: args => ({
    components: {
      BaseButton
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
          <BaseButton
            v-bind="args"
            :size="s"
            label="Label"
          />
        </div>
      </div>
    \`
  })
}`,...(C=(V=c.parameters)==null?void 0:V.docs)==null?void 0:C.source}}};var z,_,N;d.parameters={...d.parameters,docs:{...(z=d.parameters)==null?void 0:z.docs,source:{originalSource:`{
  render: args => ({
    components: {
      BaseButton
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
              <BaseButton
                v-bind="{ ...args, ...v.props }"
                :size="s"
              />
            </div>
          </div>
        </div>
      </div>
    \`
  })
}`,...(N=(_=d.parameters)==null?void 0:_.docs)==null?void 0:N.source}}};var A,P,R;p.parameters={...p.parameters,docs:{...(A=p.parameters)==null?void 0:A.docs,source:{originalSource:`{
  render: args => ({
    components: {
      BaseButton
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
          <BaseButton
            :variant="v"
            v-bind="args"
            label="Default"
          />
          <BaseButton
            :variant="v"
            v-bind="args"
            :disabled="true"
            label="Disabled"
          />
        </div>
      </div>
    \`
  })
}`,...(R=(P=p.parameters)==null?void 0:P.docs)==null?void 0:R.source}}};var q,E,D;u.parameters={...u.parameters,docs:{...(q=u.parameters)==null?void 0:q.docs,source:{originalSource:`{
  render: () => ({
    components: {
      BaseButton
    },
    template: \`
      <BaseButton
        as="a"
        href="https://www.csplab.beta.gouv.fr"
        target="_blank"
        label="Visit CSPLab"
        icon="ri:external-link-line"
      />
    \`
  })
}`,...(D=(E=u.parameters)==null?void 0:E.docs)==null?void 0:D.source}}};const de=["Default","Variants","Sizes","Icons","States","AsLink"];export{u as AsLink,i as Default,d as Icons,c as Sizes,p as States,l as Variants,de as __namedExportsOrder,ce as default};
