import{k as E,h as u,j as q,S as A,g as R,e as P,N as j,x as D,v as Z,b as O,E as m}from"./vue.esm-bundler-aFrwtEYQ.js";import{I as $}from"./iconify-LI3XAFZD.js";import{_ as K}from"./_plugin-vue_export-helper-DlAUqK2U.js";const W={key:0},Y={class:"badge__label"},T=E({__name:"CspBadge",props:{size:{default:"md"},variant:{default:"default"},label:{},type:{},icon:{},color:{}},setup(e){const s=e,c=O(()=>{if(s.type)switch(s.type){case"info":return"ri:information-fill";case"new":return"ri:flashlight-fill";case"warning":return"ri:alert-fill";case"error":return"ri:spam-fill";case"success":return"ri:checkbox-circle-fill"}return s.icon?s.icon:null});return(G,H)=>(m(),u("p",{class:Z(["badge",[`badge--${e.variant}`,`badge--${e.size}`,{[`badge--type-${e.type}`]:!!e.type},{"badge--custom-color":!!e.color}]]),style:D({color:e.color??void 0})},[c.value?(m(),u("span",W,[q(A($),{icon:c.value,width:12,height:12,"aria-hidden":"true",class:"badge__icon"},null,8,["icon"])])):R("",!0),P("span",Y,j(s.label),1)],6))}}),n=K(T,[["__scopeId","data-v-5f0b3cc0"]]);T.__docgenInfo={exportName:"default",displayName:"CspBadge",type:1,props:[{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"}],events:[],slots:[],exposed:[],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspBadge/CspBadge.vue"};const U={title:"Éléments/Génériques/CspBadge",component:n,tags:["autodocs"],parameters:{controls:{include:["variant","size","label","type","icon","color"]},docs:{description:{component:"Badge générique pour afficher des statuts ou états"}}},argTypes:{variant:{control:{type:"radio"},options:["default","soft","outline"],description:"Variant de style du badge.",table:{type:{summary:"default | soft | outline"},defaultValue:{summary:"default"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille du badge.",table:{type:{summary:"sm | md | lg"},defaultValue:{summary:"md"}}},label:{control:{type:"text"},description:"Texte visible à l'intérieur du badge.",table:{type:{summary:"string"}}},type:{control:{type:"radio"},options:["info","success","new","warning","error"],description:"Type de badge préconfiguré avec des couleurs et icônes par défaut. Ne peut pas être utilisé conjointement avec les props `icon` ou `color`.",table:{type:{summary:"info | success | new | warning | error"}}},icon:{control:{type:"text"},description:'Icone personnalisée à afficher à côté du label. Doit être une référence d\'icône compatible avec le composant `CspIcon` (ex: "ri:settings-3-line"). Ne peut pas être utilisé conjointement avec les props `type` ou `color`.',table:{type:{summary:"string"}}},color:{control:{type:"text"},description:'Couleur personnalisée pour le badge. Peut être n\'importe quelle valeur de couleur CSS valide (ex: "red", "#ff0000", "rgb(255, 0, 0)"). Ne peut pas être utilisé conjointement avec la prop `type`.',table:{type:{summary:"string"}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:"default",size:"md",label:"Libellé badge"},render:e=>({components:{CspBadge:n},setup(){return{args:e}},template:'<CspBadge v-bind="args" />'})},p=["default","soft","outline"],d=["sm","md","lg"],F=["info","success","new","warning","error"],a={args:{label:"Libellé badge"}},r={render:e=>({components:{CspBadge:n},setup(){return{variants:p,args:e}},template:`
      <div class="flex gap-12 flex-wrap">
      <div
        v-for="v in variants"
        :key="v"
      >
        <p class="mb-2">{{ v }}</p>
        <CspBadge
          v-bind="args"
          :variant="v"
          label="Libellé badge"
        />
      </div>
      </div>
    `})},t={render:e=>({components:{CspBadge:n},setup(){return{sizes:d,args:e}},template:`
      <div class="flex gap-12 flex-wrap">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <CspBadge
            v-bind="args"
            :size="s"
            label="Libellé badge"
          />
        </div>
      </div>
    `})},o={render:e=>({components:{CspBadge:n},setup(){return{sizes:d,args:e}},template:`
      <div class="flex gap-12 flex-wrap">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <CspBadge
            v-bind="args"
            :size="s"
            label="Libellé badge"
            icon="ri:settings-3-line"
          />
        </div>
      </div>
    `})},l={render:e=>({components:{CspBadge:n},setup(){return{variants:p,sizes:d,args:e}},template:`
      <div class="flex flex-col gap-12">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <div class="flex gap-8 flex-wrap">
            <CspBadge
              v-for="s in sizes"
              :key="s"
              v-bind="args"
              :variant="v"
              :size="s"
              label="Libellé badge"
              color="purple"
            />
          </div>
        </div>
      </div>
    `})},i={render:e=>({components:{CspBadge:n},setup(){return{variants:p,types:F,args:e}},template:`
      <div class="flex gap-12 flex-wrap">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <div class="flex gap-8 flex-wrap">
            <CspBadge
              v-for="t in types"
              :key="t"
              v-bind="args"
              :variant="v"
              :type="t"
              label="Libellé badge"
            />
          </div>
        </div>
      </div>
    `})};var v,g,f;a.parameters={...a.parameters,docs:{...(v=a.parameters)==null?void 0:v.docs,source:{originalSource:`{
  args: {
    label: 'Libellé badge'
  }
}`,...(f=(g=a.parameters)==null?void 0:g.docs)==null?void 0:f.source}}};var b,y,x;r.parameters={...r.parameters,docs:{...(b=r.parameters)==null?void 0:b.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspBadge
    },
    setup() {
      return {
        variants: VARIANTS,
        args
      };
    },
    template: \`
      <div class="flex gap-12 flex-wrap">
      <div
        v-for="v in variants"
        :key="v"
      >
        <p class="mb-2">{{ v }}</p>
        <CspBadge
          v-bind="args"
          :variant="v"
          label="Libellé badge"
        />
      </div>
      </div>
    \`
  })
}`,...(x=(y=r.parameters)==null?void 0:y.docs)==null?void 0:x.source}}};var C,k,B;t.parameters={...t.parameters,docs:{...(C=t.parameters)==null?void 0:C.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspBadge
    },
    setup() {
      return {
        sizes: SIZES,
        args
      };
    },
    template: \`
      <div class="flex gap-12 flex-wrap">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <CspBadge
            v-bind="args"
            :size="s"
            label="Libellé badge"
          />
        </div>
      </div>
    \`
  })
}`,...(B=(k=t.parameters)==null?void 0:k.docs)==null?void 0:B.source}}};var w,z,S;o.parameters={...o.parameters,docs:{...(w=o.parameters)==null?void 0:w.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspBadge
    },
    setup() {
      return {
        sizes: SIZES,
        args
      };
    },
    template: \`
      <div class="flex gap-12 flex-wrap">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <CspBadge
            v-bind="args"
            :size="s"
            label="Libellé badge"
            icon="ri:settings-3-line"
          />
        </div>
      </div>
    \`
  })
}`,...(S=(z=o.parameters)==null?void 0:z.docs)==null?void 0:S.source}}};var h,I,N;l.parameters={...l.parameters,docs:{...(h=l.parameters)==null?void 0:h.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspBadge
    },
    setup() {
      return {
        variants: VARIANTS,
        sizes: SIZES,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-12">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <div class="flex gap-8 flex-wrap">
            <CspBadge
              v-for="s in sizes"
              :key="s"
              v-bind="args"
              :variant="v"
              :size="s"
              label="Libellé badge"
              color="purple"
            />
          </div>
        </div>
      </div>
    \`
  })
}`,...(N=(I=l.parameters)==null?void 0:I.docs)==null?void 0:N.source}}};var _,V,L;i.parameters={...i.parameters,docs:{...(_=i.parameters)==null?void 0:_.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspBadge
    },
    setup() {
      return {
        variants: VARIANTS,
        types: TYPES,
        args
      };
    },
    template: \`
      <div class="flex gap-12 flex-wrap">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <div class="flex gap-8 flex-wrap">
            <CspBadge
              v-for="t in types"
              :key="t"
              v-bind="args"
              :variant="v"
              :type="t"
              label="Libellé badge"
            />
          </div>
        </div>
      </div>
    \`
  })
}`,...(L=(V=i.parameters)==null?void 0:V.docs)==null?void 0:L.source}}};const X=["Default","Variants","Sizes","CustomIcon","CustomColor","WithType"];export{l as CustomColor,o as CustomIcon,a as Default,t as Sizes,r as Variants,i as WithType,X as __namedExportsOrder,U as default};
