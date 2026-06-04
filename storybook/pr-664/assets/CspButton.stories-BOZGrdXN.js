import{F as j,h as b,C as M,m as E,c as H,i as m,d as J,x as Q,a as U,q as f,z as W,f as g,w as X,e as C,g as Y}from"./vue.esm-bundler-D28085mC.js";import{_ as ee}from"./CspIcon-CnKlg7n7.js";function O(e){return e?e.flatMap(n=>n.type===j?O(n.children):[n]):[]}const ne=b({name:"PrimitiveSlot",inheritAttrs:!1,setup(e,{attrs:n,slots:a}){return()=>{var y;if(!a.default)return null;const t=O(a.default()),r=t.findIndex(K=>K.type!==M);if(r===-1)return t;const o=t[r];(y=o.props)==null||delete y.ref;const $=o.props?E(n,o.props):n,v=H({...o,props:{}},$);return t.length===1?v:(t[r]=v,t)}}}),te=["area","img","input"],ae=b({name:"Primitive",inheritAttrs:!1,props:{asChild:{type:Boolean,default:!1},as:{type:[String,Object],default:"div"}},setup(e,{attrs:n,slots:a}){const t=e.asChild?"template":e.as;return typeof t=="string"&&te.includes(t)?()=>m(t,n):t!=="template"?()=>m(e.as,n,{default:a.default}):()=>m(ne,n,{default:a.default})}}),se={key:0,class:"csp-btn__label"},re={key:1,class:"btn__icon"},F=b({__name:"CspButton",props:{asChild:{type:Boolean},as:{default:"button"},variant:{default:"primary"},size:{default:"md"},isIconLeft:{type:Boolean,default:!1},label:{},icon:{}},setup(e){const n=e,a=U(()=>!!n.icon&&!n.label);return(t,r)=>(f(),J(Q(ae),E(n,{class:["csp-btn",[`csp-btn--${e.variant}`,`csp-btn--${e.size}`,{"csp-btn--icon-only":a.value},{"csp-btn--icon-left":!a.value&&e.isIconLeft&&!!e.icon},{"csp-btn--icon-right":!a.value&&!e.isIconLeft&&!!e.icon}]]}),{default:W(()=>[e.label?(f(),g("span",se,X(e.label),1)):C("",!0),e.icon?(f(),g("span",re,[Y(ee,{class:"csp-btn__icon",name:e.icon},null,8,["name"])])):C("",!0)]),_:1},16,["class"]))}}),oe=(e,n)=>{const a=e.__vccOpts||e;for(const[t,r]of n)a[t]=r;return a},s=oe(F,[["__scopeId","data-v-aa4cac9c"]]);F.__docgenInfo={exportName:"default",displayName:"CspButton",type:1,props:[{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"}],events:[],slots:[],exposed:[],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspButton/CspButton.vue"};const ce={title:"Élements/Génériques/BaseButton",component:s,tags:["autodocs"],parameters:{controls:{include:["variant","size","isIconLeft","label","icon","as","asChild"]},docs:{description:{component:"Bouton générique. Doit avoir un `label`, une `icon`, ou les deux."}}},argTypes:{variant:{control:{type:"radio"},options:["primary","secondary","tertiary","tertiary-no-outline"],description:"Style visuel.",table:{type:{summary:"primary | secondary | tertiary | tertiary-no-outline"},defaultValue:{summary:"primary"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille du bouton.",table:{type:{summary:"sm | md | lg"},defaultValue:{summary:"md"}}},isIconLeft:{control:{type:"boolean"},description:"Afficher l'icône avant le libellé.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},label:{control:{type:"text"},description:"Texte du bouton. Requis si `icon` est absent.",table:{type:{summary:"string"}}},icon:{control:{type:"text"},description:"Nom Iconify. Requis si `label` est absent.",table:{type:{summary:"string"}}},as:{control:{type:"text"},description:"Élément ou composant rendu.",table:{type:{summary:"string | Component"},defaultValue:{summary:"button"}}},asChild:{control:{type:"boolean"},description:"Rendre l'enfant comme élément racine.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:"primary",size:"md",isIconLeft:!1,label:"Libellé du bouton",asChild:!1},render:e=>({components:{CspButton:s},setup(){return{args:e}},template:'<CspButton v-bind="args" />'})},G=["primary","secondary","tertiary","tertiary-no-outline"],Z=["sm","md","lg"],i={args:{label:"Button label"}},l={render:e=>({components:{CspButton:s},setup(){return{variants:G,args:e}},template:`
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
    `})},c={render:e=>({components:{CspButton:s},setup(){return{sizes:Z,args:e}},template:`
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
    `})},p={render:e=>({components:{CspButton:s},setup(){return{args:e,iconVariants:[{description:"No icon",props:{label:"Label"}},{description:"Icon right",props:{label:"Label",icon:"ri:arrow-right-line"}},{description:"Icon left",props:{label:"Label",icon:"ri:arrow-left-line",isIconLeft:!0}},{description:"Icon only",props:{icon:"ri:checkbox-circle-line",label:void 0}}],sizes:Z}},template:`
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
    `})},d={render:e=>({components:{CspButton:s},setup(){return{variants:G,args:e}},template:`
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
    `})},u={render:()=>({components:{CspButton:s},template:`
      <CspButton
        as="a"
        href="https://www.csplab.beta.gouv.fr"
        target="_blank"
        label="Visit CSPLab"
        icon="ri:external-link-line"
      />
    `})};var x,h,B;i.parameters={...i.parameters,docs:{...(x=i.parameters)==null?void 0:x.docs,source:{originalSource:`{
  args: {
    label: 'Button label'
  }
}`,...(B=(h=i.parameters)==null?void 0:h.docs)==null?void 0:B.source}}};var k,I,S;l.parameters={...l.parameters,docs:{...(k=l.parameters)==null?void 0:k.docs,source:{originalSource:`{
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
}`,...(S=(I=l.parameters)==null?void 0:I.docs)==null?void 0:S.source}}};var w,L,V;c.parameters={...c.parameters,docs:{...(w=c.parameters)==null?void 0:w.docs,source:{originalSource:`{
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
}`,...(V=(L=c.parameters)==null?void 0:L.docs)==null?void 0:V.source}}};var z,_,N;p.parameters={...p.parameters,docs:{...(z=p.parameters)==null?void 0:z.docs,source:{originalSource:`{
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
}`,...(N=(_=p.parameters)==null?void 0:_.docs)==null?void 0:N.source}}};var A,q,P;d.parameters={...d.parameters,docs:{...(A=d.parameters)==null?void 0:A.docs,source:{originalSource:`{
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
}`,...(P=(q=d.parameters)==null?void 0:q.docs)==null?void 0:P.source}}};var R,D,T;u.parameters={...u.parameters,docs:{...(R=u.parameters)==null?void 0:R.docs,source:{originalSource:`{
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
}`,...(T=(D=u.parameters)==null?void 0:D.docs)==null?void 0:T.source}}};const pe=["Default","Variants","Sizes","Icons","States","AsLink"];export{u as AsLink,i as Default,p as Icons,c as Sizes,d as States,l as Variants,pe as __namedExportsOrder,ce as default};
