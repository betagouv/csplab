import{i as e}from"./preload-helper-DXs2ar-j.js";import{B as t,C as n,F as r,Ft as i,L as a,Lt as o,Mt as s,P as c,R as l,Rt as u,V as d,n as f,t as p,tt as m}from"./iframe-umJqIcjw.js";import{n as h,t as g}from"./_plugin-vue_export-helper-BWZZ3XGR.js";var _,v,y,b=e((()=>{n(),f(),_={key:0},v={class:`badge__label`},y=d({__name:`CspBadge`,props:{size:{default:`md`},variant:{default:`default`},label:{},type:{},icon:{},color:{}},setup(e){let n=e,d=c(()=>{if(n.type)switch(n.type){case`info`:return`ri:information-fill`;case`new`:return`ri:flashlight-fill`;case`warning`:return`ri:alert-fill`;case`error`:return`ri:spam-fill`;case`success`:return`ri:checkbox-circle-fill`}return n.icon?n.icon:null});return(c,f)=>(m(),l(`p`,{class:i([`badge`,[`badge--${e.variant}`,`badge--${e.size}`,{[`badge--type-${e.type}`]:!!e.type},{"badge--custom-color":!!e.color}]]),style:o({color:e.color??void 0})},[d.value?(m(),l(`span`,_,[t(s(p),{icon:d.value,width:12,height:12,"aria-hidden":`true`,class:`badge__icon`},null,8,[`icon`])])):a(``,!0),r(`span`,v,u(n.label),1)],6))}})})),x=e((()=>{})),S,C=e((()=>{b(),b(),x(),h(),S=g(y,[[`__scopeId`,`data-v-5f0b3cc0`]]),y.__docgenInfo=Object.assign({displayName:y.name??y.__name},{exportName:`default`,displayName:`CspBadge`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspBadge/CspBadge.vue`})})),w,T,E,D,O,k,A,j,M,N,P;e((()=>{C(),w={title:`Éléments/Génériques/CspBadge`,component:S,tags:[`autodocs`],parameters:{controls:{include:[`variant`,`size`,`label`,`type`,`icon`,`color`]},docs:{description:{component:`Badge générique pour afficher des statuts ou états`}}},argTypes:{variant:{control:{type:`radio`},options:[`default`,`soft`,`outline`],description:`Variant de style du badge.`,table:{type:{summary:`default | soft | outline`},defaultValue:{summary:`default`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille du badge.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},label:{control:{type:`text`},description:`Texte visible à l'intérieur du badge.`,table:{type:{summary:`string`}}},type:{control:{type:`radio`},options:[`info`,`success`,`new`,`warning`,`error`],description:"Type de badge préconfiguré avec des couleurs et icônes par défaut. Ne peut pas être utilisé conjointement avec les props `icon` ou `color`.",table:{type:{summary:`info | success | new | warning | error`}}},icon:{control:{type:`text`},description:'Icone personnalisée à afficher à côté du label. Doit être une référence d\'icône compatible avec le composant `CspIcon` (ex: "ri:settings-3-line"). Ne peut pas être utilisé conjointement avec les props `type` ou `color`.',table:{type:{summary:`string`}}},color:{control:{type:`text`},description:'Couleur personnalisée pour le badge. Peut être n\'importe quelle valeur de couleur CSS valide (ex: "red", "#ff0000", "rgb(255, 0, 0)"). Ne peut pas être utilisé conjointement avec la prop `type`.',table:{type:{summary:`string`}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:`default`,size:`md`,label:`Libellé badge`},render:e=>({components:{CspBadge:S},setup(){return{args:e}},template:`<CspBadge v-bind="args" />`})},T=[`default`,`soft`,`outline`],E=[`sm`,`md`,`lg`],D=[`info`,`success`,`new`,`warning`,`error`],O={args:{label:`Libellé badge`}},k={render:e=>({components:{CspBadge:S},setup(){return{variants:T,args:e}},template:`
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
    `})},A={render:e=>({components:{CspBadge:S},setup(){return{sizes:E,args:e}},template:`
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
    `})},j={render:e=>({components:{CspBadge:S},setup(){return{sizes:E,args:e}},template:`
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
    `})},M={render:e=>({components:{CspBadge:S},setup(){return{variants:T,sizes:E,args:e}},template:`
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
    `})},N={render:e=>({components:{CspBadge:S},setup(){return{variants:T,types:D,args:e}},template:`
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
    `})},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{
  args: {
    label: 'Libellé badge'
  }
}`,...O.parameters?.docs?.source}}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{
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
}`,...k.parameters?.docs?.source}}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`{
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
}`,...A.parameters?.docs?.source}}},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
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
}`,...j.parameters?.docs?.source}}},M.parameters={...M.parameters,docs:{...M.parameters?.docs,source:{originalSource:`{
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
}`,...M.parameters?.docs?.source}}},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
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
}`,...N.parameters?.docs?.source}}},P=[`Default`,`Variants`,`Sizes`,`CustomIcon`,`CustomColor`,`WithType`]}))();export{M as CustomColor,j as CustomIcon,O as Default,A as Sizes,k as Variants,N as WithType,P as __namedExportsOrder,w as default};