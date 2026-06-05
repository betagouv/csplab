import{F as j,h as v,C as M,m as O,c as H,i as m,d as J,x as Q,a as U,q as f,z as W,f as g,w as X,e as C,g as Y}from"./vue.esm-bundler-D28085mC.js";import{_ as ee}from"./CspIcon-CnKlg7n7.js";function D(e){return e?e.flatMap(n=>n.type===j?D(n.children):[n]):[]}const ne=v({name:"PrimitiveSlot",inheritAttrs:!1,setup(e,{attrs:n,slots:s}){return()=>{var y;if(!s.default)return null;const t=D(s.default()),r=t.findIndex(K=>K.type!==M);if(r===-1)return t;const o=t[r];(y=o.props)==null||delete y.ref;const $=o.props?O(n,o.props):n,b=H({...o,props:{}},$);return t.length===1?b:(t[r]=b,t)}}}),te=["area","img","input"],se=v({name:"Primitive",inheritAttrs:!1,props:{asChild:{type:Boolean,default:!1},as:{type:[String,Object],default:"div"}},setup(e,{attrs:n,slots:s}){const t=e.asChild?"template":e.as;return typeof t=="string"&&te.includes(t)?()=>m(t,n):t!=="template"?()=>m(e.as,n,{default:s.default}):()=>m(ne,n,{default:s.default})}}),ae={key:0,class:"csp-btn__label"},re={key:1,class:"btn__icon"},F=v({__name:"CspButton",props:{asChild:{type:Boolean},as:{default:"button"},variant:{default:"primary"},size:{default:"md"},isIconLeft:{type:Boolean,default:!1},label:{},icon:{}},setup(e){const n=e,s=U(()=>!!n.icon&&!n.label);return(t,r)=>(f(),J(Q(se),O(n,{class:["csp-btn",[`csp-btn--${e.variant}`,`csp-btn--${e.size}`,{"csp-btn--icon-only":s.value},{"csp-btn--icon-left":!s.value&&e.isIconLeft&&!!e.icon},{"csp-btn--icon-right":!s.value&&!e.isIconLeft&&!!e.icon}]]}),{default:W(()=>[e.label?(f(),g("span",ae,X(e.label),1)):C("",!0),e.icon?(f(),g("span",re,[Y(ee,{class:"csp-btn__icon",name:e.icon},null,8,["name"])])):C("",!0)]),_:1},16,["class"]))}}),oe=(e,n)=>{const s=e.__vccOpts||e;for(const[t,r]of n)s[t]=r;return s},a=oe(F,[["__scopeId","data-v-451c7689"]]);F.__docgenInfo={exportName:"default",displayName:"CspButton",type:1,props:[{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"}],events:[],slots:[],exposed:[],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspButton/CspButton.vue"};const ce={title:"Éléments/Génériques/CspButton",component:a,tags:["autodocs"],parameters:{controls:{include:["variant","size","isIconLeft","label","icon","as","asChild"]},docs:{description:{component:"Bouton générique. Doit avoir un `label`, une `icon`, ou les deux."}}},argTypes:{variant:{control:{type:"radio"},options:["primary","secondary","tertiary","tertiary-no-outline"],description:"Style visuel.",table:{type:{summary:"primary | secondary | tertiary | tertiary-no-outline"},defaultValue:{summary:"primary"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille du bouton.",table:{type:{summary:"sm | md | lg"},defaultValue:{summary:"md"}}},isIconLeft:{control:{type:"boolean"},description:"Afficher l'icône avant le libellé.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},label:{control:{type:"text"},description:"Texte du bouton. Requis si `icon` est absent.",table:{type:{summary:"string"}}},icon:{control:{type:"text"},description:"Nom Iconify. Requis si `label` est absent.",table:{type:{summary:"string"}}},as:{control:{type:"text"},description:"Élément ou composant rendu.",table:{type:{summary:"string | Component"},defaultValue:{summary:"button"}}},asChild:{control:{type:"boolean"},description:"Rendre l'enfant comme élément racine.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:"primary",size:"md",isIconLeft:!1,label:"Libellé du bouton",asChild:!1},render:e=>({components:{CspButton:a},setup(){return{args:e}},template:'<CspButton v-bind="args" />'})},G=["primary","secondary","tertiary","tertiary-no-outline"],Z=["sm","md","lg"],i={args:{label:"Button label"}},l={render:e=>({components:{CspButton:a},setup(){return{variants:G,args:e}},template:`
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
    `})},c={render:e=>({components:{CspButton:a},setup(){return{sizes:Z,args:e}},template:`
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
    `})},p={render:e=>({components:{CspButton:a},setup(){return{args:e,iconVariants:[{description:"No icon",props:{label:"Label"}},{description:"Icon right",props:{label:"Label",icon:"ri:arrow-right-line"}},{description:"Icon left",props:{label:"Label",icon:"ri:arrow-left-line",isIconLeft:!0}},{description:"Icon only",props:{icon:"ri:checkbox-circle-line",label:void 0}}],sizes:Z}},template:`
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
    `})},d={render:e=>({components:{CspButton:a},setup(){return{variants:G,args:e}},template:`
      <div class="flex flex-col gap-3">
        <div
          v-for="v in variants"
          :key="v"
          class="flex gap-3 items-center"
        >
          <p class="w-24">{{ v }}</p>
          <CspButton
            v-bind="args"
            :variant="v"
            label="Activé"
          />
          <CspButton
            v-bind="args"
            :variant="v"
            :disabled="true"
            label="Désactivé"
          />
        </div>
      </div>
    `})},u={render:()=>({components:{CspButton:a},template:`
      <CspButton
        as="a"
        href="https://www.csplab.beta.gouv.fr"
        target="_blank"
        label="Visit CSPLab"
        icon="ri:external-link-line"
      />
    `})};var x,h,k;i.parameters={...i.parameters,docs:{...(x=i.parameters)==null?void 0:x.docs,source:{originalSource:`{
  args: {
    label: 'Button label'
  }
}`,...(k=(h=i.parameters)==null?void 0:h.docs)==null?void 0:k.source}}};var B,I,S;l.parameters={...l.parameters,docs:{...(B=l.parameters)==null?void 0:B.docs,source:{originalSource:`{
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
            v-bind="args"
            :variant="v"
            label="Activé"
          />
          <CspButton
            v-bind="args"
            :variant="v"
            :disabled="true"
            label="Désactivé"
          />
        </div>
      </div>
    \`
  })
}`,...(P=(q=d.parameters)==null?void 0:q.docs)==null?void 0:P.source}}};var R,T,E;u.parameters={...u.parameters,docs:{...(R=u.parameters)==null?void 0:R.docs,source:{originalSource:`{
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
}`,...(E=(T=u.parameters)==null?void 0:T.docs)==null?void 0:E.source}}};const pe=["Default","Variants","Sizes","Icons","States","AsLink"];export{u as AsLink,i as Default,p as Icons,c as Sizes,d as States,l as Variants,pe as __namedExportsOrder,ce as default};
