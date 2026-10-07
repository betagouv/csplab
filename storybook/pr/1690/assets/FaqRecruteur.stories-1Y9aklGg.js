import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{i as t,n,r,t as i}from"./CspAccordionItem-BfWtFsqH.js";import{n as a,r as o,t as s}from"./faq-BSVuVKrU.js";function c(e){return`
  <CspAccordionItem
    v-for="entree in ${e}"
    :key="entree.id"
    :value="entree.id"
    :title="entree.question"
  >
    <p style="margin: 0 0 0.75rem; white-space: pre-line">{{ entree.reponse }}</p>
    <p style="margin: 0; font-size: 0.875rem; color: var(--text-mention-grey)">
      <strong>Où :</strong> {{ entree.ou }}
    </p>
  </CspAccordionItem>
`}var l,u,d,f;function p(){return(p=e((()=>{t(),n(),o(),l={title:`Compositions/ATS/Aide — FAQ recruteur`,component:r,tags:[`autodocs`],parameters:{layout:`padded`,controls:{disable:!0},docs:{description:{component:`FAQ recruteur de la page Aide : CspAccordion composé avec les entrées réelles de la feature (constants/faq.ts), un accordéon par thème, rendu comme dans AideView.`}}}},u={name:`Thème Démarrer (première entrée dépliée)`,render:()=>({components:{CspAccordion:r,CspAccordionItem:i},setup(){let e=s.filter(e=>e.theme===`Démarrer`);return{entrees:e,premiere:e[0]?.id}},template:`
      <CspAccordion :default-value="premiere ? [premiere] : undefined">
        ${c(`entrees`)}
      </CspAccordion>
    `})},d={name:`Toutes les entrées`,render:()=>({components:{CspAccordion:r,CspAccordionItem:i},setup(){return{sections:a.map((e,t)=>({id:`aide-theme-${t}`,titre:e,entrees:s.filter(t=>t.theme===e)}))}},template:`
      <section
        v-for="(section, index) in sections"
        :key="section.id"
        :style="index > 0 ? 'margin-top: 2rem' : undefined"
      >
        <h2
          :id="section.id"
          style="margin: 0 0 0.75rem; font-size: 1.25rem; font-weight: 700; color: var(--text-title-grey)"
        >
          {{ section.titre }}
        </h2>
        <CspAccordion>
          ${c(`section.entrees`)}
        </CspAccordion>
      </section>
    `})},f=[`ThemeDemarrer`,`ToutesLesEntrees`],u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Thème Démarrer (première entrée dépliée)',
  render: () => ({
    components: {
      CspAccordion,
      CspAccordionItem
    },
    setup() {
      const entrees = FAQ_ENTREES.filter(entree => entree.theme === 'Démarrer');
      return {
        entrees,
        premiere: entrees[0]?.id
      };
    },
    template: \`
      <CspAccordion :default-value="premiere ? [premiere] : undefined">
        \${entreesTemplate('entrees')}
      </CspAccordion>
    \`
  })
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Toutes les entrées',
  render: () => ({
    components: {
      CspAccordion,
      CspAccordionItem
    },
    setup() {
      const sections = FAQ_THEMES.map((titre, index) => ({
        id: \`aide-theme-\${index}\`,
        titre,
        entrees: FAQ_ENTREES.filter(entree => entree.theme === titre)
      }));
      return {
        sections
      };
    },
    template: \`
      <section
        v-for="(section, index) in sections"
        :key="section.id"
        :style="index > 0 ? 'margin-top: 2rem' : undefined"
      >
        <h2
          :id="section.id"
          style="margin: 0 0 0.75rem; font-size: 1.25rem; font-weight: 700; color: var(--text-title-grey)"
        >
          {{ section.titre }}
        </h2>
        <CspAccordion>
          \${entreesTemplate('section.entrees')}
        </CspAccordion>
      </section>
    \`
  })
}`,...d.parameters?.docs?.source}}}})))()}p();export{u as ThemeDemarrer,d as ToutesLesEntrees,f as __namedExportsOrder,l as default};