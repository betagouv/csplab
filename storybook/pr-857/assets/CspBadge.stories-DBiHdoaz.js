import{i as e}from"./preload-helper-VAmZrhww.js";import{n as t,t as n}from"./CspBadge-BgVlfcv_.js";var r,i,a,o,s,c,l,u,d,f,p;e((()=>{t(),r={title:`Éléments/Génériques/CspBadge`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`variant`,`size`,`label`,`type`,`icon`,`color`]},docs:{description:{component:`Badge générique pour afficher des statuts ou états`}}},argTypes:{variant:{control:{type:`radio`},options:[`default`,`soft`,`outline`],description:`Variant de style du badge.`,table:{type:{summary:`default | soft | outline`},defaultValue:{summary:`default`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille du badge.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},label:{control:{type:`text`},description:`Texte visible à l'intérieur du badge.`,table:{type:{summary:`string`}}},type:{control:{type:`radio`},options:[`info`,`success`,`new`,`warning`,`error`],description:"Type de badge préconfiguré avec des couleurs et icônes par défaut. Ne peut pas être utilisé conjointement avec les props `icon` ou `color`.",table:{type:{summary:`info | success | new | warning | error`}}},icon:{control:{type:`text`},description:'Icone personnalisée à afficher à côté du label. Doit être une référence d\'icône compatible avec le composant `CspIcon` (ex: "ri:settings-3-line"). Ne peut pas être utilisé conjointement avec les props `type` ou `color`.',table:{type:{summary:`string`}}},color:{control:{type:`text`},description:'Couleur personnalisée pour le badge. Peut être n\'importe quelle valeur de couleur CSS valide (ex: "red", "#ff0000", "rgb(255, 0, 0)"). Ne peut pas être utilisé conjointement avec la prop `type`.',table:{type:{summary:`string`}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:`default`,size:`md`,label:`Libellé badge`},render:e=>({components:{CspBadge:n},setup(){return{args:e}},template:`<CspBadge v-bind="args" />`})},i=[`default`,`soft`,`outline`],a=[`sm`,`md`,`lg`],o=[`info`,`success`,`new`,`warning`,`error`],s={args:{label:`Libellé badge`}},c={render:e=>({components:{CspBadge:n},setup(){return{variants:i,args:e}},template:`
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
    `})},l={render:e=>({components:{CspBadge:n},setup(){return{sizes:a,args:e}},template:`
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
    `})},u={render:e=>({components:{CspBadge:n},setup(){return{sizes:a,args:e}},template:`
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
    `})},d={render:e=>({components:{CspBadge:n},setup(){return{variants:i,sizes:a,args:e}},template:`
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
    `})},f={render:e=>({components:{CspBadge:n},setup(){return{variants:i,types:o,args:e}},template:`
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
    `})},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
  args: {
    label: 'Libellé badge'
  }
}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
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
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
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
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
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
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
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
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
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
}`,...f.parameters?.docs?.source}}},p=[`Default`,`Variants`,`Sizes`,`CustomIcon`,`CustomColor`,`WithType`]}))();export{d as CustomColor,u as CustomIcon,s as Default,l as Sizes,c as Variants,f as WithType,p as __namedExportsOrder,r as default};