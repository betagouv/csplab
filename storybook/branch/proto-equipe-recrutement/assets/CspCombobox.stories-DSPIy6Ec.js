import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{_t as t,l as n,x as r}from"./iframe-C0OAurLG.js";import{n as i,t as a}from"./CspCombobox-C8Q8DkjY.js";function o(e){return{components:{CspCombobox:a},setup(){let n=t(null),i=t(``);return{args:e,model:n,searchTerm:i,filtered:r(()=>{let e=i.value.trim().toLowerCase();return e?s.filter(t=>t.label.toLowerCase().includes(e)):s})}},template:`
      <div style="max-width: 24rem; min-height: 18rem;">
        <CspCombobox
          v-bind="args"
          v-model="model"
          v-model:search-term="searchTerm"
          :options="filtered"
        />
        <p style="margin-top: 1rem; font-size: 0.8125rem; color: var(--text-mention-grey);">
          Sélection : {{ model ?? 'aucune' }}
        </p>
      </div>
    `}}var s,c,l,u,d;function f(){return(f=e((()=>{n(),i(),s=[{value:`option-1`,label:`Option 1`,description:`Description de l'option 1`},{value:`option-2`,label:`Option 2`,description:`Description de l'option 2`},{value:`option-3`,label:`Option 3`,description:`Description de l'option 3`},{value:`option-4`,label:`Option 4`}],c={title:`Éléments/Génériques/CspCombobox`,component:a,tags:[`autodocs`],parameters:{controls:{include:[`label`,`hint`,`placeholder`,`emptyLabel`,`actionLabel`,`pending`]},docs:{description:{component:"Champ de recherche avec autocomplétion, construit sur la primitive `reka-ui` Combobox (pattern ARIA combobox : focus conservé dans le champ, navigation par `aria-activedescendant`, annonce du nombre de résultats via une région de statut). Le filtrage est à la charge de l'appelant (`searchTerm` en v-model). Une option d'action facultative (`actionLabel`) s'affiche en fin de liste et émet `action` sans sélectionner de valeur."}}},argTypes:{options:{control:!1,description:"Options affichées. Chaque option a une `value`, un `label` et une `description` optionnelle.",table:{type:{summary:`CspComboboxOption[]`}}},label:{control:{type:`text`},description:`Libellé du champ.`,table:{type:{summary:`string`}}},hint:{control:{type:`text`},description:"Texte d'aide sous le libellé, relié au champ par `aria-describedby`.",table:{type:{summary:`string`}}},actionLabel:{control:{type:`text`},description:"Libellé de l'option d'action en fin de liste. `null` pour la masquer.",table:{type:{summary:`string | null`}}}},args:{options:s,label:`Rechercher un élément`,placeholder:`Rechercher…`}},l={render:e=>o(e)},u={name:`Avec option d'action`,render:e=>o({...e,actionLabel:`Créer un nouvel élément`}),parameters:{docs:{description:{story:"L'option d'action apparaît en fin de liste, séparée des résultats. Elle émet `action` au lieu de sélectionner une valeur."}}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  render: args => renderCombobox(args)
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Avec option d\\'action',
  render: args => renderCombobox({
    ...args,
    actionLabel: 'Créer un nouvel élément'
  }),
  parameters: {
    docs: {
      description: {
        story: 'L\\'option d\\'action apparaît en fin de liste, séparée des résultats. Elle émet \`action\` au lieu de sélectionner une valeur.'
      }
    }
  }
}`,...u.parameters?.docs?.source}}},d=[`Default`,`AvecAction`]})))()}f();export{u as AvecAction,l as Default,d as __namedExportsOrder,c as default};