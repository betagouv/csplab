import{i as e}from"./preload-helper-Ct_ODC0V.js";import{$ as t,At as n,B as r,Bt as i,D as a,F as o,G as s,H as c,K as l,Lt as u,Ut as d,V as f,W as p,ct as m,gt as h,mt as g,ot as _,pt as v,yt as y}from"./iframe-B7Id9pSu.js";import{n as b,t as x}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as S,t as C}from"./CspIcon-CEbS1EjI.js";import{Q as w,X as T,ct as E,et as D,ft as O,gt as k,it as A,mt as j,nt as M,ot as N,t as P,ut as F}from"./dist-Coe3ymXI.js";var I,L,R,z=e((()=>{a(),P(),S(),I=[`for`],L={key:1,class:`csp-select-group__error`,role:`alert`},R=l({__name:`CspSelect`,props:t({options:{},placeholder:{default:`Sélectionner…`},size:{default:`md`},disabled:{type:Boolean,default:!1},error:{type:Boolean,default:!1},errorMessage:{},id:{default:()=>v()},label:{}},{modelValue:{},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let t=g(e,`modelValue`);return(n,a)=>(_(),c(`div`,{class:i([`csp-select-group`,{"csp-select-group--error":e.error}])},[e.label?(_(),c(`label`,{key:0,class:`csp-select-group__label`,for:e.id},d(e.label),9,I)):f(``,!0),s(u(k),{modelValue:t.value,"onUpdate:modelValue":a[0]||=e=>t.value=e,disabled:e.disabled},{default:y(()=>[s(u(D),{id:e.id,class:i([`csp-select`,[`csp-select--${e.size}`,{"csp-select--error":e.error}]]),"aria-invalid":e.error||void 0},{default:y(()=>[s(u(w),{placeholder:e.placeholder},null,8,[`placeholder`]),s(C,{class:`csp-select__chevron`,name:`ri:arrow-down-s-line`})]),_:1},8,[`id`,`class`,`aria-invalid`]),s(u(N),null,{default:y(()=>[s(u(j),{class:`csp-select-content`,position:`popper`,"side-offset":4},{default:y(()=>[s(u(M),{class:`csp-select-content__scroll-btn`},{default:y(()=>[s(C,{name:`ri:arrow-up-s-line`})]),_:1}),s(u(T),{class:`csp-select-content__viewport`},{default:y(()=>[(_(!0),c(o,null,m(e.options,e=>(_(),r(u(O),{key:e.value,class:`csp-select-content__item`,value:e.value,disabled:e.disabled},{default:y(()=>[s(u(E),null,{default:y(()=>[p(d(e.label),1)]),_:2},1024),s(u(F),{class:`csp-select-content__item-indicator`},{default:y(()=>[s(C,{name:`ri:check-line`})]),_:1})]),_:2},1032,[`value`,`disabled`]))),128))]),_:1}),s(u(A),{class:`csp-select-content__scroll-btn`},{default:y(()=>[s(C,{name:`ri:arrow-down-s-line`})]),_:1})]),_:1})]),_:1})]),_:1},8,[`modelValue`,`disabled`]),e.error&&e.errorMessage?(_(),c(`p`,L,[s(C,{name:`ri:error-warning-fill`,size:14}),p(` `+d(e.errorMessage),1)])):f(``,!0)],2))}})})),B=e((()=>{})),V,H=e((()=>{z(),z(),B(),b(),V=x(R,[[`__scopeId`,`data-v-3d6fe604`]]),R.__docgenInfo=Object.assign({displayName:R.name??R.__name},{exportName:`default`,displayName:`CspSelect`,type:1,props:[{name:`options`,global:!1,description:``,tags:[],required:!0,type:`{ value: string; label: string; disabled?: boolean; }[]`,declarations:[],schema:{kind:`array`,type:`{ value: string; label: string; disabled?: boolean; }[]`}},{name:`placeholder`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"S\\u00E9lectionner\\u2026"`},{name:`size`,global:!1,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg"`,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]},default:`"md"`},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`error`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`errorMessage`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`id`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`useId()`},{name:`label`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`modelValue`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: string]`,signature:`(event: "update:modelValue", value: string): void`,declarations:[],schema:[`string`]}],slots:[],exposed:[{name:`error`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`size`,type:`"md" | "sm" | "lg"`,description:``,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`disabled`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`id`,type:`string`,description:``,declarations:[],schema:`string`},{name:`placeholder`,type:`string`,description:``,declarations:[],schema:`string`},{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`modelValue`,type:`string`,description:``,declarations:[],schema:`string`},{name:`options`,type:`{ value: string; label: string; disabled?: boolean; }[]`,description:``,declarations:[],schema:{kind:`array`,type:`{ value: string; label: string; disabled?: boolean; }[]`}},{name:`errorMessage`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspSelect/CspSelect.vue`})})),U,W,G,K,q,J,Y;e((()=>{a(),H(),U=[{value:`option-1`,label:`Option 1`},{value:`option-2`,label:`Option 2`},{value:`option-3`,label:`Option 3`},{value:`option-4`,label:`Option 4`},{value:`option-5`,label:`Option 5`,disabled:!0}],W={title:`Éléments/Génériques/CspSelect`,component:V,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`options`,`placeholder`,`size`,`disabled`,`error`,`errorMessage`,`label`]},docs:{description:{component:"Sélecteur générique construit sur la primitive `reka-ui` Select. Gère le focus, la navigation clavier et l'accessibilité. Contrôlé via `v-model`."}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur sélectionnée (v-model).`,table:{type:{summary:`string`}}},options:{control:!1,description:"Liste des options. Chaque option a une `value`, un `label` et un `disabled` optionnel.",table:{type:{summary:`CspSelectOption[]`}}},placeholder:{control:{type:`text`},description:`Texte affiché quand aucune valeur n'est sélectionnée.`,table:{type:{summary:`string`},defaultValue:{summary:`Sélectionner…`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille du déclencheur.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},disabled:{control:{type:`boolean`},description:`Désactive le sélecteur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},error:{control:{type:`boolean`},description:`Affiche l'état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur affiché sous le sélecteur si `error` est vrai.",table:{type:{summary:`string`}}},label:{control:{type:`text`},description:`Libellé visible au-dessus du sélecteur.`,table:{type:{summary:`string`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{options:U,placeholder:`Sélectionner…`,size:`md`,disabled:!1,error:!1,label:`Libellé sélecteur`},render:e=>({components:{CspSelect:V},setup(){let t=n(e.modelValue??``);return h(()=>e.modelValue,e=>{t.value=e??``}),{args:e,value:t}},template:`
      <div class="max-w-xs">
        <CspSelect v-bind="args" v-model="value" />
      </div>
    `})},G=[`sm`,`md`,`lg`],K={name:`Par défaut`},q={name:`Tailles`,render:e=>({components:{CspSelect:V},setup(){return{args:e,sizes:G,options:U}},template:`
      <div class="flex flex-col gap-6 max-w-xs">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-xs text-text-mention-grey">{{ s }}</p>
          <CspSelect v-bind="args" :size="s" :options="options" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},J={name:`États`,render:()=>({components:{CspSelect:V},setup(){return{options:U}},template:`
      <div class="flex flex-col gap-8 max-w-xs">
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Par défaut</p>
          <CspSelect label="Libellé sélecteur" :options="options" placeholder="Sélectionner…" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Sélecteur avec valeur sélectionnée</p>
          <CspSelect label="Libellé sélecteur" :options="options" model-value="option-1" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Désactivé</p>
          <CspSelect label="Libellé sélecteur" :options="options" placeholder="Désactivé" :disabled="true" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Erreur</p>
          <CspSelect
            label="Libellé sélecteur"
            :options="options"
            :error="true"
            error-message="Ce champ est requis."
            placeholder="Sélectionner…"
          />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},K.parameters={...K.parameters,docs:{...K.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...K.parameters?.docs?.source}}},q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{
  name: 'Tailles',
  render: (args: CspSelectProps) => ({
    components: {
      CspSelect
    },
    setup() {
      return {
        args,
        sizes: SIZES,
        options: DEMO_OPTIONS
      };
    },
    template: \`
      <div class="flex flex-col gap-6 max-w-xs">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-xs text-text-mention-grey">{{ s }}</p>
          <CspSelect v-bind="args" :size="s" :options="options" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
  name: 'États',
  render: () => ({
    components: {
      CspSelect
    },
    setup() {
      return {
        options: DEMO_OPTIONS
      };
    },
    template: \`
      <div class="flex flex-col gap-8 max-w-xs">
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Par défaut</p>
          <CspSelect label="Libellé sélecteur" :options="options" placeholder="Sélectionner…" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Sélecteur avec valeur sélectionnée</p>
          <CspSelect label="Libellé sélecteur" :options="options" model-value="option-1" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Désactivé</p>
          <CspSelect label="Libellé sélecteur" :options="options" placeholder="Désactivé" :disabled="true" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Erreur</p>
          <CspSelect
            label="Libellé sélecteur"
            :options="options"
            :error="true"
            error-message="Ce champ est requis."
            placeholder="Sélectionner…"
          />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...J.parameters?.docs?.source}}},Y=[`Default`,`Sizes`,`States`]}))();export{K as Default,q as Sizes,J as States,Y as __namedExportsOrder,W as default};