import{i as e}from"./preload-helper-SzpdW7oQ.js";import{B as t,D as n,G as r,It as i,Q as a,at as o,ct as s,kt as c,pt as l,vt as u}from"./iframe-Civ8IDZq.js";import{n as d,t as f}from"./_plugin-vue_export-helper-syQKK5qc.js";import{t as p,v as m}from"./dist-BzE9EUuT.js";import{i as h,n as g,r as _,t as v}from"./CspTag-D9VqT7pK.js";var y,b=e((()=>{n(),p(),_(),y=r({__name:`CspTagGroup`,props:a({type:{default:`multiple`},size:{},disabled:{type:Boolean,default:!1},loop:{type:Boolean,default:!0}},{modelValue:{},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let n=e,r=l(e,`modelValue`);return h({size:n.size,disabled:n.disabled}),(n,a)=>(o(),t(i(m),{modelValue:r.value,"onUpdate:modelValue":a[0]||=e=>r.value=e,class:`csp-tag-group`,type:e.type,disabled:e.disabled,loop:e.loop,"roving-focus":!0},{default:u(()=>[s(n.$slots,`default`,{},void 0,!0)]),_:3},8,[`modelValue`,`type`,`disabled`,`loop`]))}})})),x=e((()=>{})),S,C=e((()=>{b(),b(),x(),d(),S=f(y,[[`__scopeId`,`data-v-53ec5618`]]),y.__docgenInfo=Object.assign({displayName:y.name??y.__name},{exportName:`default`,displayName:`CspTagGroup`,type:2,props:[{name:`type`,global:!1,description:``,tags:[],required:!1,type:`"single" | "multiple"`,declarations:[],schema:{kind:`enum`,type:`"single" | "multiple"`,schema:[`"single"`,`"multiple"`]},default:`"multiple"`},{name:`size`,global:!1,description:``,tags:[],required:!1,type:`CspTagSize`,declarations:[],schema:{kind:`enum`,type:`CspTagSize`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`loop`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`modelValue`,global:!1,description:``,tags:[],required:!1,type:`string | number | (string | number)[]`,declarations:[],schema:{kind:`enum`,type:`string | number | (string | number)[]`,schema:[`string`,`number`,{kind:`array`,type:`(string | number)[]`}]}},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: string | number | (string | number)[]]`,signature:`(evt: "update:modelValue", value: string | number | (string | number)[]): void`,declarations:[],schema:[{kind:`enum`,type:`string | number | (string | number)[]`,schema:[`string`,`number`,{kind:`array`,type:`(string | number)[]`}]}]}],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTag/CspTagGroup.vue`})})),w,T,E,D,O,k,A,j,M,N,P;e((()=>{n(),g(),C(),w={title:`Éléments/Génériques/CspTag`,component:v,tags:[`autodocs`],parameters:{controls:{include:[`label`,`variant`,`size`,`icon`,`pressed`,`disabled`,`href`,`value`,`dismissLabel`]},docs:{description:{component:"Étiquette générique. Sert à **catégoriser ou filtrer** les contenus (à ne pas confondre avec `CspBadge` qui signale un état).\n\nConstruit sur les primitives [reka-ui](https://reka-ui.com) :\n- `static` et `clickable` reposent sur le composant `Primitive` de reka et sont polymorphes via `as` / `asChild` ;\n- `dismissible` est toujours un `<button>` ;\n- `selectable` repose sur le composant reka `Toggle` rendu seul, ou sur `ToggleGroupItem` lorsqu'il est placé dans un `CspTagGroup`.\n"}}},argTypes:{label:{control:{type:`text`},description:`Libellé du tag (cas simple). Pour un contenu riche, utiliser le slot par défaut.`,table:{type:{summary:`string`}}},variant:{control:{type:`radio`},options:[`static`,`clickable`,`selectable`,`dismissible`],description:`Mode d'interaction du tag.`,table:{type:{summary:`static | clickable | selectable | dismissible`},defaultValue:{summary:`static`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:"Taille du tag. Héritée du `CspTagGroup` si non précisée.",table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},icon:{control:{type:`text`},description:"Icône Iconify affichée à gauche. Non disponible sur `dismissible` (croix exclusive).",table:{type:{summary:`string`}}},pressed:{control:{type:`boolean`},description:"État activé du tag `selectable` autonome. Lier avec `v-model:pressed`.",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},disabled:{control:{type:`boolean`},description:"Désactive les variantes interactives. Héritée du `CspTagGroup`.",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},href:{control:{type:`text`},description:"URL cible pour la variante `clickable`. Rend un `<a>` si fourni, sinon un `<button>`.",table:{type:{summary:`string`}}},value:{control:{type:`text`},description:"Identifiant d'un tag `selectable` au sein d'un `CspTagGroup`.",table:{type:{summary:`string | number`}}},dismissLabel:{control:{type:`text`},description:"Label accessible du bouton de suppression (`dismissible`). Par défaut : `Retirer le filtre {label}`.",table:{type:{summary:`string`}}},as:{control:!1,table:{disable:!0}},asChild:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{label:`Libellé`,variant:`static`,size:`md`,pressed:!1,disabled:!1},render:e=>({components:{CspTag:v},setup(){return{args:e,pressed:c(!!e.pressed)}},template:`
      <CspTag
        v-bind="args"
        v-model:pressed="pressed"
        @dismiss="() => {}"
      />
    `})},T=[`sm`,`md`,`lg`],E={name:`Par défaut`},D={name:`Variantes`,render:()=>({components:{CspTag:v},setup(){return{pressed:c(!1),dismissed:c(!1)}},template:`
      <div class="flex flex-col gap-6">
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">static (étiquette)</p>
          <CspTag label="Catégorie" variant="static" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">clickable (lien)</p>
          <CspTag label="Voir tout" variant="clickable" href="#" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">selectable (filtre à bascule / {{ pressed ? 'actif' : 'inactif' }})</p>
          <CspTag label="Filtre A" variant="selectable" v-model:pressed="pressed" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">dismissible : filtre actif à retirer</p>
          <CspTag v-if="!dismissed" label="Filtre actif" variant="dismissible" @dismiss="dismissed = true" />
          <span v-else class="text-sm text-text-mention-grey italic">retiré</span>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},O={name:`Avec icône`,render:()=>({components:{CspTag:v},template:`
      <div class="flex flex-row gap-4 flex-wrap">
        <CspTag label="Étiquette" variant="static" icon="ri:bookmark-line" />
        <CspTag label="Lien" variant="clickable" icon="ri:external-link-line" href="#" />
        <CspTag label="Filtre" variant="selectable" icon="ri:filter-line" />
      </div>
    `}),parameters:{controls:{disable:!0}}},k={name:`Tailles`,render:()=>({components:{CspTag:v},setup(){return{sizes:T}},template:`
      <div class="flex flex-col gap-6">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-sm text-text-mention-grey">{{ s }}</p>
          <div class="flex flex-row gap-3 flex-wrap">
            <CspTag :label="'Étiquette ' + s" :size="s" variant="static" />
            <CspTag :label="'Lien ' + s" :size="s" variant="clickable" href="#" />
            <CspTag :label="'Filtre ' + s" :size="s" variant="selectable" />
            <CspTag :label="'Sélectionné ' + s" :size="s" variant="selectable" :pressed="true" />
            <CspTag :label="'Actif ' + s" :size="s" variant="dismissible" />
          </div>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},A={name:`Sélectionnable (autonome)`,render:()=>({components:{CspTag:v},setup(){return{a:c(!1),b:c(!0),c:c(!1)}},template:`
      <div class="flex flex-col gap-3">
        <p class="text-sm text-text-mention-grey">Tags <code>selectable</code> autonomes : chacun son <code>v-model:pressed</code>.</p>
        <div class="flex flex-row gap-2 flex-wrap">
          <CspTag label="Design" variant="selectable" v-model:pressed="a" />
          <CspTag label="Développement" variant="selectable" v-model:pressed="b" />
          <CspTag label="Produit" variant="selectable" v-model:pressed="c" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},j={name:`Sélectionnable (groupe)`,render:()=>({components:{CspTag:v,CspTagGroup:S},setup(){return{single:c(`dev`),multiple:c([`design`,`data`]),domains:[{value:`design`,label:`Design`},{value:`dev`,label:`Développement`},{value:`produit`,label:`Produit`},{value:`data`,label:`Data`}]}},template:`
    <p class="text-sm mb-2 text-text-mention-grey">(navigable avec les flèches directionnelles)</p>
      <div class="flex flex-col gap-6">
        <div class="flex flex-col gap-2">
          <p class="text-sm text-text-mention-grey">Groupe multiple</p>
          <CspTagGroup v-model="multiple" type="multiple">
            <CspTag
              v-for="d in domains"
              :key="d.value"
              :value="d.value"
              :label="d.label"
              variant="selectable"
            />
          </CspTagGroup>
        </div>
        <div class="flex flex-col gap-2">
          <p class="text-sm text-text-mention-grey">Groupe single</p>
          <CspTagGroup v-model="single" type="single">
            <CspTag
              v-for="d in domains"
              :key="d.value"
              :value="d.value"
              :label="d.label"
              variant="selectable"
            />
          </CspTagGroup>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},M={name:`Supprimable`,render:()=>({components:{CspTag:v},setup(){return{active:c([`Accessibilité`,`Vue`,`TypeScript`])}},template:`
      <div class="flex flex-col gap-3">
        <p class="text-sm text-text-mention-grey">Filtres actifs :</p>
        <div class="flex flex-row gap-2 flex-wrap">
          <CspTag
            v-for="label in active"
            :key="label"
            :label="label"
            variant="dismissible"
            @dismiss="active = active.filter(l => l !== label)"
          />
          <span v-if="active.length === 0" class="text-sm text-text-mention-grey italic">Aucun filtre actif</span>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},N={name:`États`,render:()=>({components:{CspTag:v},template:`
      <div class="flex flex-col gap-4">
        <div class="flex flex-row gap-3 flex-wrap items-center">
          <p class="w-28 text-sm text-text-mention-grey">Normal</p>
          <CspTag label="Clickable" variant="clickable" href="#" />
          <CspTag label="Sélectionnable" variant="selectable" />
          <CspTag label="Sélectionné" variant="selectable" :pressed="true" />
          <CspTag label="Actif" variant="dismissible" />
        </div>
        <div class="flex flex-row gap-3 flex-wrap items-center">
          <p class="w-28 text-sm text-text-mention-grey">Désactivé</p>
          <CspTag label="Clickable" variant="clickable" :disabled="true" />
          <CspTag label="Sélectionnable" variant="selectable" :disabled="true" />
          <CspTag label="Sélectionné" variant="selectable" :pressed="true" :disabled="true" />
          <CspTag label="Supprimable" variant="dismissible" :disabled="true" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},E.parameters={...E.parameters,docs:{...E.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...E.parameters?.docs?.source}}},D.parameters={...D.parameters,docs:{...D.parameters?.docs,source:{originalSource:`{
  name: 'Variantes',
  render: () => ({
    components: {
      CspTag
    },
    setup() {
      const pressed = ref(false);
      const dismissed = ref(false);
      return {
        pressed,
        dismissed
      };
    },
    template: \`
      <div class="flex flex-col gap-6">
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">static (étiquette)</p>
          <CspTag label="Catégorie" variant="static" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">clickable (lien)</p>
          <CspTag label="Voir tout" variant="clickable" href="#" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">selectable (filtre à bascule / {{ pressed ? 'actif' : 'inactif' }})</p>
          <CspTag label="Filtre A" variant="selectable" v-model:pressed="pressed" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">dismissible : filtre actif à retirer</p>
          <CspTag v-if="!dismissed" label="Filtre actif" variant="dismissible" @dismiss="dismissed = true" />
          <span v-else class="text-sm text-text-mention-grey italic">retiré</span>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...D.parameters?.docs?.source}}},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{
  name: 'Avec icône',
  render: () => ({
    components: {
      CspTag
    },
    template: \`
      <div class="flex flex-row gap-4 flex-wrap">
        <CspTag label="Étiquette" variant="static" icon="ri:bookmark-line" />
        <CspTag label="Lien" variant="clickable" icon="ri:external-link-line" href="#" />
        <CspTag label="Filtre" variant="selectable" icon="ri:filter-line" />
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...O.parameters?.docs?.source}}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{
  name: 'Tailles',
  render: () => ({
    components: {
      CspTag
    },
    setup() {
      return {
        sizes: SIZES
      };
    },
    template: \`
      <div class="flex flex-col gap-6">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-sm text-text-mention-grey">{{ s }}</p>
          <div class="flex flex-row gap-3 flex-wrap">
            <CspTag :label="'Étiquette ' + s" :size="s" variant="static" />
            <CspTag :label="'Lien ' + s" :size="s" variant="clickable" href="#" />
            <CspTag :label="'Filtre ' + s" :size="s" variant="selectable" />
            <CspTag :label="'Sélectionné ' + s" :size="s" variant="selectable" :pressed="true" />
            <CspTag :label="'Actif ' + s" :size="s" variant="dismissible" />
          </div>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...k.parameters?.docs?.source}}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`{
  name: 'Sélectionnable (autonome)',
  render: () => ({
    components: {
      CspTag
    },
    setup() {
      const a = ref(false);
      const b = ref(true);
      const c = ref(false);
      return {
        a,
        b,
        c
      };
    },
    template: \`
      <div class="flex flex-col gap-3">
        <p class="text-sm text-text-mention-grey">Tags <code>selectable</code> autonomes : chacun son <code>v-model:pressed</code>.</p>
        <div class="flex flex-row gap-2 flex-wrap">
          <CspTag label="Design" variant="selectable" v-model:pressed="a" />
          <CspTag label="Développement" variant="selectable" v-model:pressed="b" />
          <CspTag label="Produit" variant="selectable" v-model:pressed="c" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...A.parameters?.docs?.source}}},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
  name: 'Sélectionnable (groupe)',
  render: () => ({
    components: {
      CspTag,
      CspTagGroup
    },
    setup() {
      const single = ref<string>('dev');
      const multiple = ref<string[]>(['design', 'data']);
      const domains = [{
        value: 'design',
        label: 'Design'
      }, {
        value: 'dev',
        label: 'Développement'
      }, {
        value: 'produit',
        label: 'Produit'
      }, {
        value: 'data',
        label: 'Data'
      }];
      return {
        single,
        multiple,
        domains
      };
    },
    template: \`
    <p class="text-sm mb-2 text-text-mention-grey">(navigable avec les flèches directionnelles)</p>
      <div class="flex flex-col gap-6">
        <div class="flex flex-col gap-2">
          <p class="text-sm text-text-mention-grey">Groupe multiple</p>
          <CspTagGroup v-model="multiple" type="multiple">
            <CspTag
              v-for="d in domains"
              :key="d.value"
              :value="d.value"
              :label="d.label"
              variant="selectable"
            />
          </CspTagGroup>
        </div>
        <div class="flex flex-col gap-2">
          <p class="text-sm text-text-mention-grey">Groupe single</p>
          <CspTagGroup v-model="single" type="single">
            <CspTag
              v-for="d in domains"
              :key="d.value"
              :value="d.value"
              :label="d.label"
              variant="selectable"
            />
          </CspTagGroup>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...j.parameters?.docs?.source}}},M.parameters={...M.parameters,docs:{...M.parameters?.docs,source:{originalSource:`{
  name: 'Supprimable',
  render: () => ({
    components: {
      CspTag
    },
    setup() {
      const active = ref(['Accessibilité', 'Vue', 'TypeScript']);
      return {
        active
      };
    },
    template: \`
      <div class="flex flex-col gap-3">
        <p class="text-sm text-text-mention-grey">Filtres actifs :</p>
        <div class="flex flex-row gap-2 flex-wrap">
          <CspTag
            v-for="label in active"
            :key="label"
            :label="label"
            variant="dismissible"
            @dismiss="active = active.filter(l => l !== label)"
          />
          <span v-if="active.length === 0" class="text-sm text-text-mention-grey italic">Aucun filtre actif</span>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...M.parameters?.docs?.source}}},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
  name: 'États',
  render: () => ({
    components: {
      CspTag
    },
    template: \`
      <div class="flex flex-col gap-4">
        <div class="flex flex-row gap-3 flex-wrap items-center">
          <p class="w-28 text-sm text-text-mention-grey">Normal</p>
          <CspTag label="Clickable" variant="clickable" href="#" />
          <CspTag label="Sélectionnable" variant="selectable" />
          <CspTag label="Sélectionné" variant="selectable" :pressed="true" />
          <CspTag label="Actif" variant="dismissible" />
        </div>
        <div class="flex flex-row gap-3 flex-wrap items-center">
          <p class="w-28 text-sm text-text-mention-grey">Désactivé</p>
          <CspTag label="Clickable" variant="clickable" :disabled="true" />
          <CspTag label="Sélectionnable" variant="selectable" :disabled="true" />
          <CspTag label="Sélectionné" variant="selectable" :pressed="true" :disabled="true" />
          <CspTag label="Supprimable" variant="dismissible" :disabled="true" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...N.parameters?.docs?.source}}},P=[`Default`,`Variants`,`WithIcon`,`Sizes`,`Selectable`,`SelectableGroup`,`Dismissible`,`States`]}))();export{E as Default,M as Dismissible,A as Selectable,j as SelectableGroup,k as Sizes,N as States,D as Variants,O as WithIcon,P as __namedExportsOrder,w as default};