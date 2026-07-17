import{i as e}from"./preload-helper-Ct_ODC0V.js";import{At as t,D as n,Ot as r,R as i}from"./iframe-93AkpITs.js";import{n as a,t as o}from"./CspPagination-CYrTI94c.js";import{n as s,t as c}from"./CspTag-DFOrVZlY.js";import{n as l,t as u}from"./CspDataTable-CPGelVZx.js";function d(){let e=t(new Set),n=i(()=>e.value.size);function r(t){let n=new Set(e.value);n.has(t)?n.delete(t):n.add(t),e.value=n}function a(t){let n=t.length>0&&t.every(t=>e.value.has(t)),r=new Set(e.value);n?t.forEach(e=>r.delete(e)):t.forEach(e=>r.add(e)),e.value=r}return{count:n,selectedIds:e,toggle:r,toggleVisible:a}}function f(e){return()=>({components:{CspDataTable:u,CspTag:c},setup(){return{columns:h,demos:r(e.map(e=>{let t=d();return{...e,count:t.count,selectedIds:t.selectedIds,onToggleRow:e=>t.toggle(e),onToggleAll:e=>t.toggleVisible(e)}}))}},template:`
      <div class="grid max-w-6xl gap-6">
        <section
          v-for="demo in demos"
          :key="demo.name"
          class="grid gap-3"
        >
          <div class="flex flex-wrap items-center justify-between gap-3">
            <p class="m-0 text-sm font-medium text-(--text-title-grey)">{{ demo.name }}</p>
            <p
              v-if="demo.selectionMode !== 'none'"
              class="m-0 text-sm text-(--text-mention-grey)"
            >
              {{ demo.count }} sélectionnée(s)
            </p>
          </div>

          <CspDataTable
            :rows="demo.rows"
            :columns="columns"
            :row-key="(row) => row.id"
            caption="Tableau de données"
            :selection-mode="demo.selectionMode"
            :selected-ids="demo.selectedIds"
            :selection-label="(row) => 'Sélectionner ' + row.libelle"
            :size="demo.size"
            :empty-label="demo.emptyLabel"
            @toggle-row="demo.onToggleRow"
            @toggle-all="demo.onToggleAll"
          >
            <template #cell-categorie="{ value }">
              <CspTag :label="String(value)" variant="static" size="sm" />
            </template>
            <template #cell-quantite="{ value }">
              <strong>{{ value }}</strong>
            </template>
          </CspDataTable>
        </section>
      </div>
    `})}var p,m,h,g,_,v,y,b,x,S,C;e((()=>{n(),a(),s(),l(),p=[{id:`1`,libelle:`Alpha`,reference:`REF-001`,categorie:`Catégorie A`,date:`15/02/26`,quantite:24},{id:`2`,libelle:`Bravo`,reference:`REF-002`,categorie:`Catégorie B`,date:`12/02/26`,quantite:18},{id:`3`,libelle:`Charlie`,reference:`REF-003`,categorie:`Catégorie A`,date:`10/02/26`,quantite:31},{id:`4`,libelle:`Delta`,reference:`REF-004`,categorie:`Catégorie C`,date:`08/02/26`,quantite:12},{id:`5`,libelle:`Echo`,reference:`REF-005`,categorie:`Catégorie B`,date:`05/02/26`,quantite:27},{id:`6`,libelle:`Foxtrot`,reference:`REF-006`,categorie:`Catégorie A`,date:`03/02/26`,quantite:9},{id:`7`,libelle:`Golf`,reference:`REF-007`,categorie:`Catégorie C`,date:`01/02/26`,quantite:15},{id:`8`,libelle:`Hotel`,reference:`REF-008`,categorie:`Catégorie B`,date:`29/01/26`,quantite:22}],m=p.slice(0,4),h=[{id:`libelle`,header:`Libellé`,sortable:!0,width:`26%`,accessor:e=>e.libelle},{id:`reference`,header:`Référence`,sortable:!0,width:`18%`,accessor:e=>e.reference},{id:`categorie`,header:`Catégorie`,sortable:!0,width:`22%`,accessor:e=>e.categorie},{id:`date`,header:`Date`,sortable:!0,width:`16%`,accessor:e=>e.date},{id:`quantite`,header:`Quantité`,sortable:!0,align:`end`,width:`18%`,accessor:e=>e.quantite}],g={title:`Compositions/Génériques/CspDataTable`,component:u,tags:[`autodocs`],parameters:{layout:`padded`,controls:{include:[`selectionMode`,`activationMode`,`size`,`pageSize`]},docs:{description:{component:"Table de données générique avec tri, densité, pagination et sélection. Les cellules riches passent par les slots `cell-*`, les en-têtes par `header-*`, et le footer reçoit le contexte de pagination."}}},argTypes:{selectionMode:{control:{type:`radio`},options:[`none`,`checkbox`,`row`],description:`Mode de sélection des lignes : aucun, case à cocher uniquement, ou clic sur toute la ligne.`,table:{defaultValue:{summary:`none`}}},activationMode:{control:{type:`radio`},options:[`none`,`row`,`cell`],description:'Mode d’activation (navigation / ouverture d’un drawer) : aucun, clic sur toute la ligne, ou clic sur une cible précise exposée via le helper `activate` du slot de cellule. `row` est ignoré si `selectionMode="row"`.',table:{defaultValue:{summary:`none`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Densité d’affichage des lignes.`,table:{defaultValue:{summary:`default`}}},pageSize:{control:{type:`number`,min:1,step:1},description:`Nombre de lignes affichées par page.`,table:{defaultValue:{summary:`5`}}}},args:{selectionMode:`row`,size:`md`,pageSize:5},render:e=>({components:{CspDataTable:u,CspPagination:o,CspTag:c},setup(){let t=d();return{args:e,columns:h,count:t.count,rows:p,selectedIds:t.selectedIds,onToggleRow:e=>t.toggle(e),onToggleAll:e=>t.toggleVisible(e)}},template:`
      <div class="flex max-w-6xl flex-col gap-3">
        <div class="flex flex-wrap items-center gap-4 text-sm text-(--text-mention-grey)">
          <span>{{ count }} sélectionnée(s)</span>
        </div>

        <CspDataTable
          :rows="rows"
          :columns="columns"
          :row-key="(row) => row.id"
          caption="Tableau de données"
          :selection-mode="args.selectionMode"
          :selected-ids="selectedIds"
          :selection-label="(row) => 'Sélectionner ' + row.libelle"
          :size="args.size"
          :page-size="args.pageSize"
          @toggle-row="onToggleRow"
          @toggle-all="onToggleAll"
        >
          <template #cell-categorie="{ value }">
            <CspTag :label="String(value)" variant="static" size="sm" />
          </template>
          <template #cell-quantite="{ value }">
            <strong>{{ value }}</strong>
          </template>
          <template #footer="pg">
            <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <p class="m-0 text-sm text-(--text-mention-grey)">
                Affichage de {{ pg.range.from }} à {{ pg.range.to }} sur {{ pg.total }} éléments
              </p>
              <CspPagination
                :page="pg.page"
                :page-count="pg.pageCount"
                :show-direction-labels="false"
                @update:page="pg.setPage"
              />
            </div>
          </template>
        </CspDataTable>
      </div>
    `})},_={name:`Par défaut`},v={name:`Tailles`,render:()=>({components:{CspDataTable:u,CspTag:c},setup(){return{columns:h,rows:m,sizes:[`sm`,`md`,`lg`]}},template:`
      <div class="grid max-w-6xl gap-6">
        <section
          v-for="s in sizes"
          :key="s"
          class="grid gap-3"
        >
          <p class="m-0 text-sm font-medium text-(--text-title-grey)">{{ s }}</p>
          <CspDataTable
            :rows="rows"
            :columns="columns"
            :row-key="(row) => row.id"
            caption="Tableau de données"
            :size="s"
          >
            <template #cell-categorie="{ value }">
              <CspTag :label="String(value)" variant="static" size="sm" />
            </template>
            <template #cell-quantite="{ value }">
              <strong>{{ value }}</strong>
            </template>
            <template #footer="pg">
              <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <p class="m-0 text-sm text-(--text-mention-grey)">
                  Affichage de {{ pg.range.from }} à {{ pg.range.to }} sur {{ pg.total }} éléments
                </p>
                <CspPagination
                  :page="pg.page"
                  :page-count="pg.pageCount"
                  :show-direction-labels="false"
                  @update:page="pg.setPage"
                />
              </div>
            </template>
          </CspDataTable>
        </section>
      </div>
    `}),parameters:{controls:{disable:!0},docs:{description:{story:`Compare rapidement les trois densités supportées par la table.`}}}},y=[{id:`libelle`,header:`Libellé du produit`,sortable:!0,accessor:e=>e.libelle},{id:`reference`,header:`Référence interne`,sortable:!0,accessor:e=>e.reference},{id:`categorie`,header:`Catégorie de classement`,sortable:!0,accessor:e=>e.categorie},{id:`date`,header:`Date de dernière mise à jour`,sortable:!0,accessor:e=>e.date},{id:`quantite`,header:`Quantité en stock`,sortable:!0,align:`end`,accessor:e=>e.quantite}],b={name:`Débordement (scroll horizontal)`,render:()=>({components:{CspDataTable:u,CspTag:c},setup(){return{columns:y,rows:m}},template:`
      <div class="max-w-md">
        <CspDataTable
          :rows="rows"
          :columns="columns"
          :row-key="(row) => row.id"
          caption="Tableau de données"
        >
          <template #cell-categorie="{ value }">
            <CspTag :label="String(value)" variant="static" size="sm" />
          </template>
          <template #cell-quantite="{ value }">
            <strong>{{ value }}</strong>
          </template>
        </CspDataTable>
      </div>
    `}),parameters:{controls:{disable:!0},docs:{description:{story:`Dans un conteneur trop étroit, la zone de contenu défile horizontalement.`}}}},x={name:`Modes de sélection`,render:f([{name:`Aucune sélection`,rows:p.slice(0,5),size:`md`,selectionMode:`none`},{name:`Sélection par checkbox`,rows:p.slice(0,5),size:`md`,selectionMode:`checkbox`},{name:`Sélection par ligne`,rows:p.slice(0,5),size:`md`,selectionMode:`row`},{name:`État vide`,rows:[],size:`md`,selectionMode:`none`,emptyLabel:`Aucun élément`}]),parameters:{controls:{disable:!0},docs:{description:{story:`Compare les trois comportements de sélection attendus : aucun, checkbox uniquement, ou sélection par clic sur toute la ligne.`}}}},S={name:`Modes d’activation`,render:()=>({components:{CspDataTable:u,CspTag:c},setup(){let e=t(null);return{columns:h,rows:p.slice(0,5),lastActivated:e,onActivate:t=>{e.value=t}}},template:`
      <div class="grid max-w-6xl gap-6">
        <p class="m-0 text-sm text-(--text-mention-grey)">
          Dernière ligne activée : <strong>{{ lastActivated ?? '—' }}</strong>
        </p>

        <section class="grid gap-3">
          <p class="m-0 text-sm font-medium text-(--text-title-grey)">
            Activation par ligne (clic n’importe où sur la ligne)
          </p>
          <CspDataTable
            :rows="rows"
            :columns="columns"
            :row-key="(row) => row.id"
            caption="Tableau de données — activation ligne"
            activation-mode="row"
            @activate="onActivate"
          >
            <template #cell-categorie="{ value }">
              <CspTag :label="String(value)" variant="static" size="sm" />
            </template>
          </CspDataTable>
        </section>

        <section class="grid gap-3">
          <p class="m-0 text-sm font-medium text-(--text-title-grey)">
            Activation par cellule (seul le libellé est cliquable)
          </p>
          <CspDataTable
            :rows="rows"
            :columns="columns"
            :row-key="(row) => row.id"
            caption="Tableau de données — activation cellule"
            activation-mode="cell"
            @activate="onActivate"
          >
            <template #cell-libelle="{ value, activate }">
              <button
                type="button"
                class="cursor-pointer border-0 bg-transparent p-0 font-medium text-(--text-action-high-blue-france) underline"
                @click.stop="activate"
              >{{ value }}</button>
            </template>
            <template #cell-categorie="{ value }">
              <CspTag :label="String(value)" variant="static" size="sm" />
            </template>
          </CspDataTable>
        </section>
      </div>
    `}),parameters:{controls:{disable:!0},docs:{description:{story:"Active une ligne (navigation ou ouverture d’un drawer) soit au clic sur toute la ligne (`row`), soit au clic sur une cible précise rendue dans un slot de cellule via le helper `activate` (`cell`). En mode `cell`, le déclencheur reste un vrai bouton focusable au clavier."}}}},_.parameters={..._.parameters,docs:{..._.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,..._.parameters?.docs?.source}}},v.parameters={...v.parameters,docs:{...v.parameters?.docs,source:{originalSource:`{
  name: 'Tailles',
  render: () => ({
    components: {
      CspDataTable,
      CspTag
    },
    setup() {
      return {
        columns: COLUMNS,
        rows: SHORT_ROWS,
        sizes: ['sm', 'md', 'lg'] as const
      };
    },
    template: \`
      <div class="grid max-w-6xl gap-6">
        <section
          v-for="s in sizes"
          :key="s"
          class="grid gap-3"
        >
          <p class="m-0 text-sm font-medium text-(--text-title-grey)">{{ s }}</p>
          <CspDataTable
            :rows="rows"
            :columns="columns"
            :row-key="(row) => row.id"
            caption="Tableau de données"
            :size="s"
          >
            <template #cell-categorie="{ value }">
              <CspTag :label="String(value)" variant="static" size="sm" />
            </template>
            <template #cell-quantite="{ value }">
              <strong>{{ value }}</strong>
            </template>
            <template #footer="pg">
              <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <p class="m-0 text-sm text-(--text-mention-grey)">
                  Affichage de {{ pg.range.from }} à {{ pg.range.to }} sur {{ pg.total }} éléments
                </p>
                <CspPagination
                  :page="pg.page"
                  :page-count="pg.pageCount"
                  :show-direction-labels="false"
                  @update:page="pg.setPage"
                />
              </div>
            </template>
          </CspDataTable>
        </section>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    },
    docs: {
      description: {
        story: 'Compare rapidement les trois densités supportées par la table.'
      }
    }
  }
}`,...v.parameters?.docs?.source}}},b.parameters={...b.parameters,docs:{...b.parameters?.docs,source:{originalSource:`{
  name: 'Débordement (scroll horizontal)',
  render: () => ({
    components: {
      CspDataTable,
      CspTag
    },
    setup() {
      return {
        columns: WIDE_COLUMNS,
        rows: SHORT_ROWS
      };
    },
    template: \`
      <div class="max-w-md">
        <CspDataTable
          :rows="rows"
          :columns="columns"
          :row-key="(row) => row.id"
          caption="Tableau de données"
        >
          <template #cell-categorie="{ value }">
            <CspTag :label="String(value)" variant="static" size="sm" />
          </template>
          <template #cell-quantite="{ value }">
            <strong>{{ value }}</strong>
          </template>
        </CspDataTable>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    },
    docs: {
      description: {
        story: 'Dans un conteneur trop étroit, la zone de contenu défile horizontalement.'
      }
    }
  }
}`,...b.parameters?.docs?.source}}},x.parameters={...x.parameters,docs:{...x.parameters?.docs,source:{originalSource:`{
  name: 'Modes de sélection',
  render: createStateGalleryRender([{
    name: 'Aucune sélection',
    rows: DEMO_ROWS.slice(0, 5),
    size: 'md',
    selectionMode: 'none'
  }, {
    name: 'Sélection par checkbox',
    rows: DEMO_ROWS.slice(0, 5),
    size: 'md',
    selectionMode: 'checkbox'
  }, {
    name: 'Sélection par ligne',
    rows: DEMO_ROWS.slice(0, 5),
    size: 'md',
    selectionMode: 'row'
  }, {
    name: 'État vide',
    rows: [],
    size: 'md',
    selectionMode: 'none',
    emptyLabel: 'Aucun élément'
  }]),
  parameters: {
    controls: {
      disable: true
    },
    docs: {
      description: {
        story: 'Compare les trois comportements de sélection attendus : aucun, checkbox uniquement, ou sélection par clic sur toute la ligne.'
      }
    }
  }
}`,...x.parameters?.docs?.source}}},S.parameters={...S.parameters,docs:{...S.parameters?.docs,source:{originalSource:`{
  name: 'Modes d’activation',
  render: () => ({
    components: {
      CspDataTable,
      CspTag
    },
    setup() {
      const lastActivated = ref<string | null>(null);
      const onActivate = (id: string): void => {
        lastActivated.value = id;
      };
      return {
        columns: COLUMNS,
        rows: DEMO_ROWS.slice(0, 5),
        lastActivated,
        onActivate
      };
    },
    template: \`
      <div class="grid max-w-6xl gap-6">
        <p class="m-0 text-sm text-(--text-mention-grey)">
          Dernière ligne activée : <strong>{{ lastActivated ?? '—' }}</strong>
        </p>

        <section class="grid gap-3">
          <p class="m-0 text-sm font-medium text-(--text-title-grey)">
            Activation par ligne (clic n’importe où sur la ligne)
          </p>
          <CspDataTable
            :rows="rows"
            :columns="columns"
            :row-key="(row) => row.id"
            caption="Tableau de données — activation ligne"
            activation-mode="row"
            @activate="onActivate"
          >
            <template #cell-categorie="{ value }">
              <CspTag :label="String(value)" variant="static" size="sm" />
            </template>
          </CspDataTable>
        </section>

        <section class="grid gap-3">
          <p class="m-0 text-sm font-medium text-(--text-title-grey)">
            Activation par cellule (seul le libellé est cliquable)
          </p>
          <CspDataTable
            :rows="rows"
            :columns="columns"
            :row-key="(row) => row.id"
            caption="Tableau de données — activation cellule"
            activation-mode="cell"
            @activate="onActivate"
          >
            <template #cell-libelle="{ value, activate }">
              <button
                type="button"
                class="cursor-pointer border-0 bg-transparent p-0 font-medium text-(--text-action-high-blue-france) underline"
                @click.stop="activate"
              >{{ value }}</button>
            </template>
            <template #cell-categorie="{ value }">
              <CspTag :label="String(value)" variant="static" size="sm" />
            </template>
          </CspDataTable>
        </section>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    },
    docs: {
      description: {
        story: 'Active une ligne (navigation ou ouverture d’un drawer) soit au clic sur toute la ligne (\`row\`), soit au clic sur une cible précise rendue dans un slot de cellule via le helper \`activate\` (\`cell\`). En mode \`cell\`, le déclencheur reste un vrai bouton focusable au clavier.'
      }
    }
  }
}`,...S.parameters?.docs?.source}}},C=[`DefaultDemo`,`Sizes`,`Overflow`,`StateVariants`,`ActivationModes`]}))();export{S as ActivationModes,_ as DefaultDemo,b as Overflow,v as Sizes,x as StateVariants,C as __namedExportsOrder,g as default};