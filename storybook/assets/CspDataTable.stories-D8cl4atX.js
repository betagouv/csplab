import{i as e}from"./preload-helper-DXs2ar-j.js";import{$ as t,At as n,Bt as r,D as i,F as a,G as o,H as s,Ht as c,J as l,K as u,Lt as d,Mt as f,N as p,Ot as m,R as h,Tt as g,Ut as _,V as ee,Vt as te,W as ne,Y as re,_t as ie,ct as ae,gt as oe,lt as v,mt as se,ot as y,z as b}from"./iframe-DBWJq8oh.js";import{n as x,t as ce}from"./_plugin-vue_export-helper-BWZZ3XGR.js";import{n as le,t as ue}from"./CspIcon-BA6no29G.js";import{n as S,t as de}from"./CspCheckbox-LPvkLwe_.js";import{n as fe,t as C}from"./CspPagination-BgmWHK1g.js";import{n as pe,t as w}from"./CspTag-B0LvQ3sG.js";function me(){return{accessor:(e,t)=>typeof e==`function`?{...t,accessorFn:e}:{...t,accessorKey:e},display:e=>e,group:e=>e}}function T(e,t){return typeof e==`function`?e(t):e}function E(e,t){return n=>{t.setState(t=>({...t,[e]:T(n,t[e])}))}}function D(e){return e instanceof Function}function he(e){return Array.isArray(e)&&e.every(e=>typeof e==`number`)}function ge(e,t){let n=[],r=e=>{e.forEach(e=>{n.push(e);let i=t(e);i!=null&&i.length&&r(i)})};return r(e),n}function O(e,t,n){let r=[],i;return a=>{let o;n.key&&n.debug&&(o=Date.now());let s=e(a);if(!(s.length!==r.length||s.some((e,t)=>r[t]!==e)))return i;r=s;let c;if(n.key&&n.debug&&(c=Date.now()),i=t(...s),n==null||n.onChange==null||n.onChange(i),n.key&&n.debug&&n!=null&&n.debug()){let e=Math.round((Date.now()-o)*100)/100,t=Math.round((Date.now()-c)*100)/100,r=t/16,i=(e,t)=>{for(e=String(e);e.length<t;)e=` `+e;return e};console.info(`%c⏱ ${i(t,5)} /${i(e,5)} ms`,`
            font-size: .6rem;
            font-weight: bold;
            color: hsl(${Math.max(0,Math.min(120-120*r,120))}deg 100% 31%);`,n?.key)}return i}}function k(e,t,n,r){return{debug:()=>e?.debugAll??e[t],key:!1,onChange:r}}function A(e,t,n,r){let i={id:`${t.id}_${n.id}`,row:t,column:n,getValue:()=>t.getValue(r),renderValue:()=>i.getValue()??e.options.renderFallbackValue,getContext:O(()=>[e,n,t,i],(e,t,n,r)=>({table:e,column:t,row:n,cell:r,getValue:r.getValue,renderValue:r.renderValue}),k(e.options,`debugCells`,`cell.getContext`))};return e._features.forEach(r=>{r.createCell==null||r.createCell(i,n,t,e)},{}),i}function j(e,t,n,r){let i={...e._getDefaultColumnDef(),...t},a=i.accessorKey,o=i.id??(a?typeof String.prototype.replaceAll==`function`?a.replaceAll(`.`,`_`):a.replace(/\./g,`_`):void 0)??(typeof i.header==`string`?i.header:void 0),s;if(i.accessorFn?s=i.accessorFn:a&&(s=a.includes(`.`)?e=>{let t=e;for(let e of a.split(`.`))t=t?.[e];return t}:e=>e[i.accessorKey]),!o)throw Error();let c={id:`${String(o)}`,accessorFn:s,parent:r,depth:n,columnDef:i,columns:[],getFlatColumns:O(()=>[!0],()=>[c,...c.columns?.flatMap(e=>e.getFlatColumns())],k(e.options,`debugColumns`,`column.getFlatColumns`)),getLeafColumns:O(()=>[e._getOrderColumnsFn()],e=>{var t;return(t=c.columns)!=null&&t.length?e(c.columns.flatMap(e=>e.getLeafColumns())):[c]},k(e.options,`debugColumns`,`column.getLeafColumns`))};for(let t of e._features)t.createColumn==null||t.createColumn(c,e);return c}function M(e,t,n){let r={id:n.id??t.id,column:t,index:n.index,isPlaceholder:!!n.isPlaceholder,placeholderId:n.placeholderId,depth:n.depth,subHeaders:[],colSpan:0,rowSpan:0,headerGroup:null,getLeafHeaders:()=>{let e=[],t=n=>{n.subHeaders&&n.subHeaders.length&&n.subHeaders.map(t),e.push(n)};return t(r),e},getContext:()=>({table:e,header:r,column:t})};return e._features.forEach(t=>{t.createHeader==null||t.createHeader(r,e)}),r}function N(e,t,n,r){let i=0,a=function(e,t){t===void 0&&(t=1),i=Math.max(i,t),e.filter(e=>e.getIsVisible()).forEach(e=>{var n;(n=e.columns)!=null&&n.length&&a(e.columns,t+1)},0)};a(e);let o=[],s=(e,t)=>{let i={depth:t,id:[r,`${t}`].filter(Boolean).join(`_`),headers:[]},a=[];e.forEach(e=>{let o=[...a].reverse()[0],s=e.column.depth===i.depth,c,l=!1;if(s&&e.column.parent?c=e.column.parent:(c=e.column,l=!0),o&&o?.column===c)o.subHeaders.push(e);else{let i=M(n,c,{id:[r,t,c.id,e?.id].filter(Boolean).join(`_`),isPlaceholder:l,placeholderId:l?`${a.filter(e=>e.column===c).length}`:void 0,depth:t,index:a.length});i.subHeaders.push(e),a.push(i)}i.headers.push(e),e.headerGroup=i}),o.push(i),t>0&&s(a,t-1)};s(t.map((e,t)=>M(n,e,{depth:i,index:t})),i-1),o.reverse();let c=e=>e.filter(e=>e.column.getIsVisible()).map(e=>{let t=0,n=0,r=[0];e.subHeaders&&e.subHeaders.length?(r=[],c(e.subHeaders).forEach(e=>{let{colSpan:n,rowSpan:i}=e;t+=n,r.push(i)})):t=1;let i=Math.min(...r);return n+=i,e.colSpan=t,e.rowSpan=n,{colSpan:t,rowSpan:n}});return c(o[0]?.headers??[]),o}function P(e){return e==null||e===``}function F(e,t,n){return(e&&e.autoRemove?e.autoRemove(t,n):!1)||t===void 0||typeof t==`string`&&!t}function _e(e,t,n){if(!(t!=null&&t.length)||!n)return e;let r=e.filter(e=>!t.includes(e.id));return n===`remove`?r:[...t.map(t=>e.find(e=>e.id===t)).filter(Boolean),...r]}function ve(e){return e||(typeof document<`u`?document:null)}function ye(){if(typeof H==`boolean`)return H;let e=!1;try{let t={get passive(){return e=!0,!1}},n=()=>{};window.addEventListener(`test`,n,t),window.removeEventListener(`test`,n)}catch{e=!1}return H=e,H}function I(e){return e.type===`touchstart`}function L(e,t){return t?t===`center`?e.getCenterVisibleLeafColumns():t===`left`?e.getLeftVisibleLeafColumns():e.getRightVisibleLeafColumns():e.getVisibleLeafColumns()}function be(e,t){let n=e.getState().rowSelection,r=[],i={},a=function(e,t){return e.map(e=>{var t;let o=xe(e,n);if(o&&(r.push(e),i[e.id]=e),(t=e.subRows)!=null&&t.length&&(e={...e,subRows:a(e.subRows)}),o)return e}).filter(Boolean)};return{rows:a(t.rows),flatRows:r,rowsById:i}}function xe(e,t){return t[e.id]??!1}function Se(e,t,n){var r;if(!((r=e.subRows)!=null&&r.length))return!1;let i=!0,a=!1;return e.subRows.forEach(e=>{if(!(a&&!i)&&(e.getCanSelect()&&(xe(e,t)?a=!0:i=!1),e.subRows&&e.subRows.length)){let n=Se(e,t);n===`all`?a=!0:(n===`some`&&(a=!0),i=!1)}}),i?`all`:a?`some`:!1}function Ce(e,t){return e===t?0:e>t?1:-1}function R(e){return typeof e==`number`?isNaN(e)||e===1/0||e===-1/0?``:String(e):typeof e==`string`?e:``}function we(e,t){let n=e.split(_t).filter(Boolean),r=t.split(_t).filter(Boolean);for(;n.length&&r.length;){let e=n.shift(),t=r.shift(),i=parseInt(e,10),a=parseInt(t,10),o=[i,a].sort();if(isNaN(o[0])){if(e>t)return 1;if(t>e)return-1;continue}if(isNaN(o[1]))return isNaN(i)?-1:1;if(i>a)return 1;if(a>i)return-1}return n.length-r.length}function Te(e){let t=[...Tt,...e._features??[]],n={_features:t},r=n._features.reduce((e,t)=>Object.assign(e,t.getDefaultOptions==null?void 0:t.getDefaultOptions(n)),{}),i=e=>n.options.mergeOptions?n.options.mergeOptions(r,e):{...r,...e},a={...e.initialState??{}};n._features.forEach(e=>{a=(e.getInitialState==null?void 0:e.getInitialState(a))??a});let o=[],s=!1,c={_features:t,options:{...r,...e},initialState:a,_queue:e=>{o.push(e),s||(s=!0,Promise.resolve().then(()=>{for(;o.length;)o.shift()();s=!1}).catch(e=>setTimeout(()=>{throw e})))},reset:()=>{n.setState(n.initialState)},setOptions:e=>{n.options=i(T(e,n.options))},getState:()=>n.options.state,setState:e=>{n.options.onStateChange==null||n.options.onStateChange(e)},_getRowId:(e,t,r)=>(n.options.getRowId==null?void 0:n.options.getRowId(e,t,r))??`${r?[r.id,t].join(`.`):t}`,getCoreRowModel:()=>(n._getCoreRowModel||=n.options.getCoreRowModel(n),n._getCoreRowModel()),getRowModel:()=>n.getPaginationRowModel(),getRow:(e,t)=>{let r=(t?n.getPrePaginationRowModel():n.getRowModel()).rowsById[e];if(!r&&(r=n.getCoreRowModel().rowsById[e],!r))throw Error();return r},_getDefaultColumnDef:O(()=>[n.options.defaultColumn],e=>(e??={},{header:e=>{let t=e.header.column.columnDef;return t.accessorKey?t.accessorKey:t.accessorFn?t.id:null},cell:e=>{var t;return((t=e.renderValue())==null||t.toString==null?void 0:t.toString())??null},...n._features.reduce((e,t)=>Object.assign(e,t.getDefaultColumnDef==null?void 0:t.getDefaultColumnDef()),{}),...e}),k(e,`debugColumns`,`_getDefaultColumnDef`)),_getColumnDefs:()=>n.options.columns,getAllColumns:O(()=>[n._getColumnDefs()],e=>{let t=function(e,r,i){return i===void 0&&(i=0),e.map(e=>{let a=j(n,e,i,r),o=e;return a.columns=o.columns?t(o.columns,a,i+1):[],a})};return t(e)},k(e,`debugColumns`,`getAllColumns`)),getAllFlatColumns:O(()=>[n.getAllColumns()],e=>e.flatMap(e=>e.getFlatColumns()),k(e,`debugColumns`,`getAllFlatColumns`)),_getAllFlatColumnsById:O(()=>[n.getAllFlatColumns()],e=>e.reduce((e,t)=>(e[t.id]=t,e),{}),k(e,`debugColumns`,`getAllFlatColumnsById`)),getAllLeafColumns:O(()=>[n.getAllColumns(),n._getOrderColumnsFn()],(e,t)=>t(e.flatMap(e=>e.getLeafColumns())),k(e,`debugColumns`,`getAllLeafColumns`)),getColumn:e=>n._getAllFlatColumnsById()[e]};Object.assign(n,c);for(let e=0;e<n._features.length;e++){let t=n._features[e];t==null||t.createTable==null||t.createTable(n)}return n}function Ee(){return e=>O(()=>[e.options.data],t=>{let n={rows:[],flatRows:[],rowsById:{}},r=function(t,i,a){i===void 0&&(i=0);let o=[];for(let c=0;c<t.length;c++){let l=je(e,e._getRowId(t[c],c,a),t[c],c,i,void 0,a?.id);if(n.flatRows.push(l),n.rowsById[l.id]=l,o.push(l),e.options.getSubRows){var s;l.originalSubRows=e.options.getSubRows(t[c],c),(s=l.originalSubRows)!=null&&s.length&&(l.subRows=r(l.originalSubRows,i+1,l))}}return o};return n.rows=r(t),n},k(e.options,`debugTable`,`getRowModel`,()=>e._autoResetPageIndex()))}function De(e){let t=[],n=e=>{var r;t.push(e),(r=e.subRows)!=null&&r.length&&e.getIsExpanded()&&e.subRows.forEach(n)};return e.rows.forEach(n),{rows:t,flatRows:e.flatRows,rowsById:e.rowsById}}function Oe(e){return e=>O(()=>[e.getState().pagination,e.getPrePaginationRowModel(),e.options.paginateExpandedRows?void 0:e.getState().expanded],(t,n)=>{if(!n.rows.length)return n;let{pageSize:r,pageIndex:i}=t,{rows:a,flatRows:o,rowsById:s}=n,c=r*i,l=c+r;a=a.slice(c,l);let u;u=e.options.paginateExpandedRows?{rows:a,flatRows:o,rowsById:s}:De({rows:a,flatRows:o,rowsById:s}),u.flatRows=[];let d=e=>{u.flatRows.push(e),e.subRows.length&&e.subRows.forEach(d)};return u.rows.forEach(d),u},k(e.options,`debugTable`,`getPaginationRowModel`))}function ke(){return e=>O(()=>[e.getState().sorting,e.getPreSortedRowModel()],(t,n)=>{if(!n.rows.length||!(t!=null&&t.length))return n;let r=e.getState().sorting,i=[],a=r.filter(t=>e.getColumn(t.id)?.getCanSort()),o={};a.forEach(t=>{let n=e.getColumn(t.id);n&&(o[t.id]={sortUndefined:n.columnDef.sortUndefined,invertSorting:n.columnDef.invertSorting,sortingFn:n.getSortingFn()})});let s=e=>{let t=e.map(e=>({...e}));return t.sort((e,t)=>{for(let n=0;n<a.length;n+=1){let r=a[n],i=o[r.id],s=i.sortUndefined,c=r?.desc??!1,l=0;if(s){let n=e.getValue(r.id),i=t.getValue(r.id),a=n===void 0,o=i===void 0;if(a||o){if(s===`first`)return a?-1:1;if(s===`last`)return a?1:-1;l=a&&o?0:a?s:-s}}if(l===0&&(l=i.sortingFn(e,t,r.id)),l!==0)return c&&(l*=-1),i.invertSorting&&(l*=-1),l}return e.index-t.index}),t.forEach(e=>{var t;i.push(e),(t=e.subRows)!=null&&t.length&&(e.subRows=s(e.subRows))}),t};return{rows:s(n.rows),flatRows:i,rowsById:n.rowsById}},k(e.options,`debugTable`,`getSortedRowModel`,()=>e._autoResetPageIndex()))}var z,Ae,je,Me,Ne,Pe,Fe,Ie,Le,Re,ze,Be,Ve,B,He,Ue,We,Ge,Ke,qe,Je,Ye,Xe,Ze,Qe,$e,et,tt,nt,V,rt,it,H,at,ot,st,ct,lt,ut,dt,ft,pt,mt,ht,gt,_t,vt,yt,bt,xt,St,Ct,U,wt,Tt,Et=e((()=>{z=`debugHeaders`,Ae={createTable:e=>{e.getHeaderGroups=O(()=>[e.getAllColumns(),e.getVisibleLeafColumns(),e.getState().columnPinning.left,e.getState().columnPinning.right],(t,n,r,i)=>{let a=r?.map(e=>n.find(t=>t.id===e)).filter(Boolean)??[],o=i?.map(e=>n.find(t=>t.id===e)).filter(Boolean)??[],s=n.filter(e=>!(r!=null&&r.includes(e.id))&&!(i!=null&&i.includes(e.id)));return N(t,[...a,...s,...o],e)},k(e.options,z,`getHeaderGroups`)),e.getCenterHeaderGroups=O(()=>[e.getAllColumns(),e.getVisibleLeafColumns(),e.getState().columnPinning.left,e.getState().columnPinning.right],(t,n,r,i)=>(n=n.filter(e=>!(r!=null&&r.includes(e.id))&&!(i!=null&&i.includes(e.id))),N(t,n,e,`center`)),k(e.options,z,`getCenterHeaderGroups`)),e.getLeftHeaderGroups=O(()=>[e.getAllColumns(),e.getVisibleLeafColumns(),e.getState().columnPinning.left],(t,n,r)=>N(t,r?.map(e=>n.find(t=>t.id===e)).filter(Boolean)??[],e,`left`),k(e.options,z,`getLeftHeaderGroups`)),e.getRightHeaderGroups=O(()=>[e.getAllColumns(),e.getVisibleLeafColumns(),e.getState().columnPinning.right],(t,n,r)=>N(t,r?.map(e=>n.find(t=>t.id===e)).filter(Boolean)??[],e,`right`),k(e.options,z,`getRightHeaderGroups`)),e.getFooterGroups=O(()=>[e.getHeaderGroups()],e=>[...e].reverse(),k(e.options,z,`getFooterGroups`)),e.getLeftFooterGroups=O(()=>[e.getLeftHeaderGroups()],e=>[...e].reverse(),k(e.options,z,`getLeftFooterGroups`)),e.getCenterFooterGroups=O(()=>[e.getCenterHeaderGroups()],e=>[...e].reverse(),k(e.options,z,`getCenterFooterGroups`)),e.getRightFooterGroups=O(()=>[e.getRightHeaderGroups()],e=>[...e].reverse(),k(e.options,z,`getRightFooterGroups`)),e.getFlatHeaders=O(()=>[e.getHeaderGroups()],e=>e.map(e=>e.headers).flat(),k(e.options,z,`getFlatHeaders`)),e.getLeftFlatHeaders=O(()=>[e.getLeftHeaderGroups()],e=>e.map(e=>e.headers).flat(),k(e.options,z,`getLeftFlatHeaders`)),e.getCenterFlatHeaders=O(()=>[e.getCenterHeaderGroups()],e=>e.map(e=>e.headers).flat(),k(e.options,z,`getCenterFlatHeaders`)),e.getRightFlatHeaders=O(()=>[e.getRightHeaderGroups()],e=>e.map(e=>e.headers).flat(),k(e.options,z,`getRightFlatHeaders`)),e.getCenterLeafHeaders=O(()=>[e.getCenterFlatHeaders()],e=>e.filter(e=>{var t;return!((t=e.subHeaders)!=null&&t.length)}),k(e.options,z,`getCenterLeafHeaders`)),e.getLeftLeafHeaders=O(()=>[e.getLeftFlatHeaders()],e=>e.filter(e=>{var t;return!((t=e.subHeaders)!=null&&t.length)}),k(e.options,z,`getLeftLeafHeaders`)),e.getRightLeafHeaders=O(()=>[e.getRightFlatHeaders()],e=>e.filter(e=>{var t;return!((t=e.subHeaders)!=null&&t.length)}),k(e.options,z,`getRightLeafHeaders`)),e.getLeafHeaders=O(()=>[e.getLeftHeaderGroups(),e.getCenterHeaderGroups(),e.getRightHeaderGroups()],(e,t,n)=>[...e[0]?.headers??[],...t[0]?.headers??[],...n[0]?.headers??[]].map(e=>e.getLeafHeaders()).flat(),k(e.options,z,`getLeafHeaders`))}},je=(e,t,n,r,i,a,o)=>{let s={id:t,index:r,original:n,depth:i,parentId:o,_valuesCache:{},_uniqueValuesCache:{},getValue:t=>{if(s._valuesCache.hasOwnProperty(t))return s._valuesCache[t];let n=e.getColumn(t);if(n!=null&&n.accessorFn)return s._valuesCache[t]=n.accessorFn(s.original,r),s._valuesCache[t]},getUniqueValues:t=>{if(s._uniqueValuesCache.hasOwnProperty(t))return s._uniqueValuesCache[t];let n=e.getColumn(t);if(n!=null&&n.accessorFn)return n.columnDef.getUniqueValues?(s._uniqueValuesCache[t]=n.columnDef.getUniqueValues(s.original,r),s._uniqueValuesCache[t]):(s._uniqueValuesCache[t]=[s.getValue(t)],s._uniqueValuesCache[t])},renderValue:t=>s.getValue(t)??e.options.renderFallbackValue,subRows:a??[],getLeafRows:()=>ge(s.subRows,e=>e.subRows),getParentRow:()=>s.parentId?e.getRow(s.parentId,!0):void 0,getParentRows:()=>{let e=[],t=s;for(;;){let n=t.getParentRow();if(!n)break;e.push(n),t=n}return e.reverse()},getAllCells:O(()=>[e.getAllLeafColumns()],t=>t.map(t=>A(e,s,t,t.id)),k(e.options,`debugRows`,`getAllCells`)),_getAllCellsByColumnId:O(()=>[s.getAllCells()],e=>e.reduce((e,t)=>(e[t.column.id]=t,e),{}),k(e.options,`debugRows`,`getAllCellsByColumnId`))};for(let t=0;t<e._features.length;t++){let n=e._features[t];n==null||n.createRow==null||n.createRow(s,e)}return s},Me={createColumn:(e,t)=>{e._getFacetedRowModel=t.options.getFacetedRowModel&&t.options.getFacetedRowModel(t,e.id),e.getFacetedRowModel=()=>e._getFacetedRowModel?e._getFacetedRowModel():t.getPreFilteredRowModel(),e._getFacetedUniqueValues=t.options.getFacetedUniqueValues&&t.options.getFacetedUniqueValues(t,e.id),e.getFacetedUniqueValues=()=>e._getFacetedUniqueValues?e._getFacetedUniqueValues():new Map,e._getFacetedMinMaxValues=t.options.getFacetedMinMaxValues&&t.options.getFacetedMinMaxValues(t,e.id),e.getFacetedMinMaxValues=()=>{if(e._getFacetedMinMaxValues)return e._getFacetedMinMaxValues()}}},Ne=(e,t,n)=>{var r,i;let a=n==null||(r=n.toString())==null?void 0:r.toLowerCase();return!!(!((i=e.getValue(t))==null||(i=i.toString())==null||(i=i.toLowerCase())==null)&&i.includes(a))},Ne.autoRemove=e=>P(e),Pe=(e,t,n)=>{var r;return!!(!((r=e.getValue(t))==null||(r=r.toString())==null)&&r.includes(n))},Pe.autoRemove=e=>P(e),Fe=(e,t,n)=>{var r;return((r=e.getValue(t))==null||(r=r.toString())==null?void 0:r.toLowerCase())===n?.toLowerCase()},Fe.autoRemove=e=>P(e),Ie=(e,t,n)=>e.getValue(t)?.includes(n),Ie.autoRemove=e=>P(e),Le=(e,t,n)=>!n.some(n=>{var r;return!((r=e.getValue(t))!=null&&r.includes(n))}),Le.autoRemove=e=>P(e)||!(e!=null&&e.length),Re=(e,t,n)=>n.some(n=>e.getValue(t)?.includes(n)),Re.autoRemove=e=>P(e)||!(e!=null&&e.length),ze=(e,t,n)=>e.getValue(t)===n,ze.autoRemove=e=>P(e),Be=(e,t,n)=>e.getValue(t)==n,Be.autoRemove=e=>P(e),Ve=(e,t,n)=>{let[r,i]=n,a=e.getValue(t);return a>=r&&a<=i},Ve.resolveFilterValue=e=>{let[t,n]=e,r=typeof t==`number`?t:parseFloat(t),i=typeof n==`number`?n:parseFloat(n),a=t===null||Number.isNaN(r)?-1/0:r,o=n===null||Number.isNaN(i)?1/0:i;if(a>o){let e=a;a=o,o=e}return[a,o]},Ve.autoRemove=e=>P(e)||P(e[0])&&P(e[1]),B={includesString:Ne,includesStringSensitive:Pe,equalsString:Fe,arrIncludes:Ie,arrIncludesAll:Le,arrIncludesSome:Re,equals:ze,weakEquals:Be,inNumberRange:Ve},He={getDefaultColumnDef:()=>({filterFn:`auto`}),getInitialState:e=>({columnFilters:[],...e}),getDefaultOptions:e=>({onColumnFiltersChange:E(`columnFilters`,e),filterFromLeafRows:!1,maxLeafRowFilterDepth:100}),createColumn:(e,t)=>{e.getAutoFilterFn=()=>{let n=t.getCoreRowModel().flatRows[0]?.getValue(e.id);return typeof n==`string`?B.includesString:typeof n==`number`?B.inNumberRange:typeof n==`boolean`||typeof n==`object`&&n?B.equals:Array.isArray(n)?B.arrIncludes:B.weakEquals},e.getFilterFn=()=>D(e.columnDef.filterFn)?e.columnDef.filterFn:e.columnDef.filterFn===`auto`?e.getAutoFilterFn():t.options.filterFns?.[e.columnDef.filterFn]??B[e.columnDef.filterFn],e.getCanFilter=()=>(e.columnDef.enableColumnFilter??!0)&&(t.options.enableColumnFilters??!0)&&(t.options.enableFilters??!0)&&!!e.accessorFn,e.getIsFiltered=()=>e.getFilterIndex()>-1,e.getFilterValue=()=>{var n;return(n=t.getState().columnFilters)==null||(n=n.find(t=>t.id===e.id))==null?void 0:n.value},e.getFilterIndex=()=>t.getState().columnFilters?.findIndex(t=>t.id===e.id)??-1,e.setFilterValue=n=>{t.setColumnFilters(t=>{let r=e.getFilterFn(),i=t?.find(t=>t.id===e.id),a=T(n,i?i.value:void 0);if(F(r,a,e))return t?.filter(t=>t.id!==e.id)??[];let o={id:e.id,value:a};return i?t?.map(t=>t.id===e.id?o:t)??[]:t!=null&&t.length?[...t,o]:[o]})}},createRow:(e,t)=>{e.columnFilters={},e.columnFiltersMeta={}},createTable:e=>{e.setColumnFilters=t=>{let n=e.getAllLeafColumns();e.options.onColumnFiltersChange==null||e.options.onColumnFiltersChange(e=>T(t,e)?.filter(e=>{let t=n.find(t=>t.id===e.id);return!(t&&F(t.getFilterFn(),e.value,t))}))},e.resetColumnFilters=t=>{e.setColumnFilters(t?[]:e.initialState?.columnFilters??[])},e.getPreFilteredRowModel=()=>e.getCoreRowModel(),e.getFilteredRowModel=()=>(!e._getFilteredRowModel&&e.options.getFilteredRowModel&&(e._getFilteredRowModel=e.options.getFilteredRowModel(e)),e.options.manualFiltering||!e._getFilteredRowModel?e.getPreFilteredRowModel():e._getFilteredRowModel())}},Ue=(e,t,n)=>n.reduce((t,n)=>{let r=n.getValue(e);return t+(typeof r==`number`?r:0)},0),We=(e,t,n)=>{let r;return n.forEach(t=>{let n=t.getValue(e);n!=null&&(r>n||r===void 0&&n>=n)&&(r=n)}),r},Ge=(e,t,n)=>{let r;return n.forEach(t=>{let n=t.getValue(e);n!=null&&(r<n||r===void 0&&n>=n)&&(r=n)}),r},Ke=(e,t,n)=>{let r,i;return n.forEach(t=>{let n=t.getValue(e);n!=null&&(r===void 0?n>=n&&(r=i=n):(r>n&&(r=n),i<n&&(i=n)))}),[r,i]},qe=(e,t)=>{let n=0,r=0;if(t.forEach(t=>{let i=t.getValue(e);i!=null&&(i=+i)>=i&&(++n,r+=i)}),n)return r/n},Je=(e,t)=>{if(!t.length)return;let n=t.map(t=>t.getValue(e));if(!he(n))return;if(n.length===1)return n[0];let r=Math.floor(n.length/2),i=n.sort((e,t)=>e-t);return n.length%2==0?(i[r-1]+i[r])/2:i[r]},Ye=(e,t)=>Array.from(new Set(t.map(t=>t.getValue(e))).values()),Xe=(e,t)=>new Set(t.map(t=>t.getValue(e))).size,Ze=(e,t)=>t.length,Qe={sum:Ue,min:We,max:Ge,extent:Ke,mean:qe,median:Je,unique:Ye,uniqueCount:Xe,count:Ze},$e={getDefaultColumnDef:()=>({aggregatedCell:e=>{var t;return((t=e.getValue())==null||t.toString==null?void 0:t.toString())??null},aggregationFn:`auto`}),getInitialState:e=>({grouping:[],...e}),getDefaultOptions:e=>({onGroupingChange:E(`grouping`,e),groupedColumnMode:`reorder`}),createColumn:(e,t)=>{e.toggleGrouping=()=>{t.setGrouping(t=>t!=null&&t.includes(e.id)?t.filter(t=>t!==e.id):[...t??[],e.id])},e.getCanGroup=()=>(e.columnDef.enableGrouping??!0)&&(t.options.enableGrouping??!0)&&(!!e.accessorFn||!!e.columnDef.getGroupingValue),e.getIsGrouped=()=>t.getState().grouping?.includes(e.id),e.getGroupedIndex=()=>t.getState().grouping?.indexOf(e.id),e.getToggleGroupingHandler=()=>{let t=e.getCanGroup();return()=>{t&&e.toggleGrouping()}},e.getAutoAggregationFn=()=>{let n=t.getCoreRowModel().flatRows[0]?.getValue(e.id);if(typeof n==`number`)return Qe.sum;if(Object.prototype.toString.call(n)===`[object Date]`)return Qe.extent},e.getAggregationFn=()=>{if(!e)throw Error();return D(e.columnDef.aggregationFn)?e.columnDef.aggregationFn:e.columnDef.aggregationFn===`auto`?e.getAutoAggregationFn():t.options.aggregationFns?.[e.columnDef.aggregationFn]??Qe[e.columnDef.aggregationFn]}},createTable:e=>{e.setGrouping=t=>e.options.onGroupingChange==null?void 0:e.options.onGroupingChange(t),e.resetGrouping=t=>{e.setGrouping(t?[]:e.initialState?.grouping??[])},e.getPreGroupedRowModel=()=>e.getFilteredRowModel(),e.getGroupedRowModel=()=>(!e._getGroupedRowModel&&e.options.getGroupedRowModel&&(e._getGroupedRowModel=e.options.getGroupedRowModel(e)),e.options.manualGrouping||!e._getGroupedRowModel?e.getPreGroupedRowModel():e._getGroupedRowModel())},createRow:(e,t)=>{e.getIsGrouped=()=>!!e.groupingColumnId,e.getGroupingValue=n=>{if(e._groupingValuesCache.hasOwnProperty(n))return e._groupingValuesCache[n];let r=t.getColumn(n);return r!=null&&r.columnDef.getGroupingValue?(e._groupingValuesCache[n]=r.columnDef.getGroupingValue(e.original),e._groupingValuesCache[n]):e.getValue(n)},e._groupingValuesCache={}},createCell:(e,t,n,r)=>{e.getIsGrouped=()=>t.getIsGrouped()&&t.id===n.groupingColumnId,e.getIsPlaceholder=()=>!e.getIsGrouped()&&t.getIsGrouped(),e.getIsAggregated=()=>{var t;return!e.getIsGrouped()&&!e.getIsPlaceholder()&&!!((t=n.subRows)!=null&&t.length)}}},et={getInitialState:e=>({columnOrder:[],...e}),getDefaultOptions:e=>({onColumnOrderChange:E(`columnOrder`,e)}),createColumn:(e,t)=>{e.getIndex=O(e=>[L(t,e)],t=>t.findIndex(t=>t.id===e.id),k(t.options,`debugColumns`,`getIndex`)),e.getIsFirstColumn=n=>L(t,n)[0]?.id===e.id,e.getIsLastColumn=n=>{let r=L(t,n);return r[r.length-1]?.id===e.id}},createTable:e=>{e.setColumnOrder=t=>e.options.onColumnOrderChange==null?void 0:e.options.onColumnOrderChange(t),e.resetColumnOrder=t=>{e.setColumnOrder(t?[]:e.initialState.columnOrder??[])},e._getOrderColumnsFn=O(()=>[e.getState().columnOrder,e.getState().grouping,e.options.groupedColumnMode],(e,t,n)=>r=>{let i=[];if(!(e!=null&&e.length))i=r;else{let t=[...e],n=[...r];for(;n.length&&t.length;){let e=t.shift(),r=n.findIndex(t=>t.id===e);r>-1&&i.push(n.splice(r,1)[0])}i=[...i,...n]}return _e(i,t,n)},k(e.options,`debugTable`,`_getOrderColumnsFn`))}},tt=()=>({left:[],right:[]}),nt={getInitialState:e=>({columnPinning:tt(),...e}),getDefaultOptions:e=>({onColumnPinningChange:E(`columnPinning`,e)}),createColumn:(e,t)=>{e.pin=n=>{let r=e.getLeafColumns().map(e=>e.id).filter(Boolean);t.setColumnPinning(e=>n===`right`?{left:(e?.left??[]).filter(e=>!(r!=null&&r.includes(e))),right:[...(e?.right??[]).filter(e=>!(r!=null&&r.includes(e))),...r]}:n===`left`?{left:[...(e?.left??[]).filter(e=>!(r!=null&&r.includes(e))),...r],right:(e?.right??[]).filter(e=>!(r!=null&&r.includes(e)))}:{left:(e?.left??[]).filter(e=>!(r!=null&&r.includes(e))),right:(e?.right??[]).filter(e=>!(r!=null&&r.includes(e)))})},e.getCanPin=()=>e.getLeafColumns().some(e=>(e.columnDef.enablePinning??!0)&&(t.options.enableColumnPinning??t.options.enablePinning??!0)),e.getIsPinned=()=>{let n=e.getLeafColumns().map(e=>e.id),{left:r,right:i}=t.getState().columnPinning,a=n.some(e=>r?.includes(e)),o=n.some(e=>i?.includes(e));return a?`left`:o?`right`:!1},e.getPinnedIndex=()=>{var n;let r=e.getIsPinned();return r?((n=t.getState().columnPinning)==null||(n=n[r])==null?void 0:n.indexOf(e.id))??-1:0}},createRow:(e,t)=>{e.getCenterVisibleCells=O(()=>[e._getAllVisibleCells(),t.getState().columnPinning.left,t.getState().columnPinning.right],(e,t,n)=>{let r=[...t??[],...n??[]];return e.filter(e=>!r.includes(e.column.id))},k(t.options,`debugRows`,`getCenterVisibleCells`)),e.getLeftVisibleCells=O(()=>[e._getAllVisibleCells(),t.getState().columnPinning.left],(e,t)=>(t??[]).map(t=>e.find(e=>e.column.id===t)).filter(Boolean).map(e=>({...e,position:`left`})),k(t.options,`debugRows`,`getLeftVisibleCells`)),e.getRightVisibleCells=O(()=>[e._getAllVisibleCells(),t.getState().columnPinning.right],(e,t)=>(t??[]).map(t=>e.find(e=>e.column.id===t)).filter(Boolean).map(e=>({...e,position:`right`})),k(t.options,`debugRows`,`getRightVisibleCells`))},createTable:e=>{e.setColumnPinning=t=>e.options.onColumnPinningChange==null?void 0:e.options.onColumnPinningChange(t),e.resetColumnPinning=t=>e.setColumnPinning(t?tt():e.initialState?.columnPinning??tt()),e.getIsSomeColumnsPinned=t=>{let n=e.getState().columnPinning;return t?!!n[t]?.length:!!(n.left?.length||n.right?.length)},e.getLeftLeafColumns=O(()=>[e.getAllLeafColumns(),e.getState().columnPinning.left],(e,t)=>(t??[]).map(t=>e.find(e=>e.id===t)).filter(Boolean),k(e.options,`debugColumns`,`getLeftLeafColumns`)),e.getRightLeafColumns=O(()=>[e.getAllLeafColumns(),e.getState().columnPinning.right],(e,t)=>(t??[]).map(t=>e.find(e=>e.id===t)).filter(Boolean),k(e.options,`debugColumns`,`getRightLeafColumns`)),e.getCenterLeafColumns=O(()=>[e.getAllLeafColumns(),e.getState().columnPinning.left,e.getState().columnPinning.right],(e,t,n)=>{let r=[...t??[],...n??[]];return e.filter(e=>!r.includes(e.id))},k(e.options,`debugColumns`,`getCenterLeafColumns`))}},V={size:150,minSize:20,maxSize:2**53-1},rt=()=>({startOffset:null,startSize:null,deltaOffset:null,deltaPercentage:null,isResizingColumn:!1,columnSizingStart:[]}),it={getDefaultColumnDef:()=>V,getInitialState:e=>({columnSizing:{},columnSizingInfo:rt(),...e}),getDefaultOptions:e=>({columnResizeMode:`onEnd`,columnResizeDirection:`ltr`,onColumnSizingChange:E(`columnSizing`,e),onColumnSizingInfoChange:E(`columnSizingInfo`,e)}),createColumn:(e,t)=>{e.getSize=()=>{let n=t.getState().columnSizing[e.id];return Math.min(Math.max(e.columnDef.minSize??V.minSize,n??e.columnDef.size??V.size),e.columnDef.maxSize??V.maxSize)},e.getStart=O(e=>[e,L(t,e),t.getState().columnSizing],(t,n)=>n.slice(0,e.getIndex(t)).reduce((e,t)=>e+t.getSize(),0),k(t.options,`debugColumns`,`getStart`)),e.getAfter=O(e=>[e,L(t,e),t.getState().columnSizing],(t,n)=>n.slice(e.getIndex(t)+1).reduce((e,t)=>e+t.getSize(),0),k(t.options,`debugColumns`,`getAfter`)),e.resetSize=()=>{t.setColumnSizing(t=>{let{[e.id]:n,...r}=t;return r})},e.getCanResize=()=>(e.columnDef.enableResizing??!0)&&(t.options.enableColumnResizing??!0),e.getIsResizing=()=>t.getState().columnSizingInfo.isResizingColumn===e.id},createHeader:(e,t)=>{e.getSize=()=>{let t=0,n=e=>{e.subHeaders.length?e.subHeaders.forEach(n):t+=e.column.getSize()??0};return n(e),t},e.getStart=()=>{if(e.index>0){let t=e.headerGroup.headers[e.index-1];return t.getStart()+t.getSize()}return 0},e.getResizeHandler=n=>{let r=t.getColumn(e.column.id),i=r?.getCanResize();return a=>{if(!r||!i||(a.persist==null||a.persist(),I(a)&&a.touches&&a.touches.length>1))return;let o=e.getSize(),s=e?e.getLeafHeaders().map(e=>[e.column.id,e.column.getSize()]):[[r.id,r.getSize()]],c=I(a)?Math.round(a.touches[0].clientX):a.clientX,l={},u=(e,n)=>{typeof n==`number`&&(t.setColumnSizingInfo(e=>{let r=t.options.columnResizeDirection===`rtl`?-1:1,i=(n-(e?.startOffset??0))*r,a=Math.max(i/(e?.startSize??0),-.999999);return e.columnSizingStart.forEach(e=>{let[t,n]=e;l[t]=Math.round(Math.max(n+n*a,0)*100)/100}),{...e,deltaOffset:i,deltaPercentage:a}}),(t.options.columnResizeMode===`onChange`||e===`end`)&&t.setColumnSizing(e=>({...e,...l})))},d=e=>u(`move`,e),f=e=>{u(`end`,e),t.setColumnSizingInfo(e=>({...e,isResizingColumn:!1,startOffset:null,startSize:null,deltaOffset:null,deltaPercentage:null,columnSizingStart:[]}))},p=ve(n),m={moveHandler:e=>d(e.clientX),upHandler:e=>{p?.removeEventListener(`mousemove`,m.moveHandler),p?.removeEventListener(`mouseup`,m.upHandler),f(e.clientX)}},h={moveHandler:e=>(e.cancelable&&(e.preventDefault(),e.stopPropagation()),d(e.touches[0].clientX),!1),upHandler:e=>{p?.removeEventListener(`touchmove`,h.moveHandler),p?.removeEventListener(`touchend`,h.upHandler),e.cancelable&&(e.preventDefault(),e.stopPropagation()),f(e.touches[0]?.clientX)}},g=ye()?{passive:!1}:!1;I(a)?(p?.addEventListener(`touchmove`,h.moveHandler,g),p?.addEventListener(`touchend`,h.upHandler,g)):(p?.addEventListener(`mousemove`,m.moveHandler,g),p?.addEventListener(`mouseup`,m.upHandler,g)),t.setColumnSizingInfo(e=>({...e,startOffset:c,startSize:o,deltaOffset:0,deltaPercentage:0,columnSizingStart:s,isResizingColumn:r.id}))}}},createTable:e=>{e.setColumnSizing=t=>e.options.onColumnSizingChange==null?void 0:e.options.onColumnSizingChange(t),e.setColumnSizingInfo=t=>e.options.onColumnSizingInfoChange==null?void 0:e.options.onColumnSizingInfoChange(t),e.resetColumnSizing=t=>{e.setColumnSizing(t?{}:e.initialState.columnSizing??{})},e.resetHeaderSizeInfo=t=>{e.setColumnSizingInfo(t?rt():e.initialState.columnSizingInfo??rt())},e.getTotalSize=()=>e.getHeaderGroups()[0]?.headers.reduce((e,t)=>e+t.getSize(),0)??0,e.getLeftTotalSize=()=>e.getLeftHeaderGroups()[0]?.headers.reduce((e,t)=>e+t.getSize(),0)??0,e.getCenterTotalSize=()=>e.getCenterHeaderGroups()[0]?.headers.reduce((e,t)=>e+t.getSize(),0)??0,e.getRightTotalSize=()=>e.getRightHeaderGroups()[0]?.headers.reduce((e,t)=>e+t.getSize(),0)??0}},H=null,at={getInitialState:e=>({columnVisibility:{},...e}),getDefaultOptions:e=>({onColumnVisibilityChange:E(`columnVisibility`,e)}),createColumn:(e,t)=>{e.toggleVisibility=n=>{e.getCanHide()&&t.setColumnVisibility(t=>({...t,[e.id]:n??!e.getIsVisible()}))},e.getIsVisible=()=>{let n=e.columns;return(n.length?n.some(e=>e.getIsVisible()):t.getState().columnVisibility?.[e.id])??!0},e.getCanHide=()=>(e.columnDef.enableHiding??!0)&&(t.options.enableHiding??!0),e.getToggleVisibilityHandler=()=>t=>{e.toggleVisibility==null||e.toggleVisibility(t.target.checked)}},createRow:(e,t)=>{e._getAllVisibleCells=O(()=>[e.getAllCells(),t.getState().columnVisibility],e=>e.filter(e=>e.column.getIsVisible()),k(t.options,`debugRows`,`_getAllVisibleCells`)),e.getVisibleCells=O(()=>[e.getLeftVisibleCells(),e.getCenterVisibleCells(),e.getRightVisibleCells()],(e,t,n)=>[...e,...t,...n],k(t.options,`debugRows`,`getVisibleCells`))},createTable:e=>{let t=(t,n)=>O(()=>[n(),n().filter(e=>e.getIsVisible()).map(e=>e.id).join(`_`)],e=>e.filter(e=>e.getIsVisible==null?void 0:e.getIsVisible()),k(e.options,`debugColumns`,t));e.getVisibleFlatColumns=t(`getVisibleFlatColumns`,()=>e.getAllFlatColumns()),e.getVisibleLeafColumns=t(`getVisibleLeafColumns`,()=>e.getAllLeafColumns()),e.getLeftVisibleLeafColumns=t(`getLeftVisibleLeafColumns`,()=>e.getLeftLeafColumns()),e.getRightVisibleLeafColumns=t(`getRightVisibleLeafColumns`,()=>e.getRightLeafColumns()),e.getCenterVisibleLeafColumns=t(`getCenterVisibleLeafColumns`,()=>e.getCenterLeafColumns()),e.setColumnVisibility=t=>e.options.onColumnVisibilityChange==null?void 0:e.options.onColumnVisibilityChange(t),e.resetColumnVisibility=t=>{e.setColumnVisibility(t?{}:e.initialState.columnVisibility??{})},e.toggleAllColumnsVisible=t=>{t??=!e.getIsAllColumnsVisible(),e.setColumnVisibility(e.getAllLeafColumns().reduce((e,n)=>({...e,[n.id]:t||!(n.getCanHide!=null&&n.getCanHide())}),{}))},e.getIsAllColumnsVisible=()=>!e.getAllLeafColumns().some(e=>!(e.getIsVisible!=null&&e.getIsVisible())),e.getIsSomeColumnsVisible=()=>e.getAllLeafColumns().some(e=>e.getIsVisible==null?void 0:e.getIsVisible()),e.getToggleAllColumnsVisibilityHandler=()=>t=>{e.toggleAllColumnsVisible(t.target?.checked)}}},ot={createTable:e=>{e._getGlobalFacetedRowModel=e.options.getFacetedRowModel&&e.options.getFacetedRowModel(e,`__global__`),e.getGlobalFacetedRowModel=()=>e.options.manualFiltering||!e._getGlobalFacetedRowModel?e.getPreFilteredRowModel():e._getGlobalFacetedRowModel(),e._getGlobalFacetedUniqueValues=e.options.getFacetedUniqueValues&&e.options.getFacetedUniqueValues(e,`__global__`),e.getGlobalFacetedUniqueValues=()=>e._getGlobalFacetedUniqueValues?e._getGlobalFacetedUniqueValues():new Map,e._getGlobalFacetedMinMaxValues=e.options.getFacetedMinMaxValues&&e.options.getFacetedMinMaxValues(e,`__global__`),e.getGlobalFacetedMinMaxValues=()=>{if(e._getGlobalFacetedMinMaxValues)return e._getGlobalFacetedMinMaxValues()}}},st={getInitialState:e=>({globalFilter:void 0,...e}),getDefaultOptions:e=>({onGlobalFilterChange:E(`globalFilter`,e),globalFilterFn:`auto`,getColumnCanGlobalFilter:t=>{var n;let r=(n=e.getCoreRowModel().flatRows[0])==null||(n=n._getAllCellsByColumnId()[t.id])==null?void 0:n.getValue();return typeof r==`string`||typeof r==`number`}}),createColumn:(e,t)=>{e.getCanGlobalFilter=()=>(e.columnDef.enableGlobalFilter??!0)&&(t.options.enableGlobalFilter??!0)&&(t.options.enableFilters??!0)&&((t.options.getColumnCanGlobalFilter==null?void 0:t.options.getColumnCanGlobalFilter(e))??!0)&&!!e.accessorFn},createTable:e=>{e.getGlobalAutoFilterFn=()=>B.includesString,e.getGlobalFilterFn=()=>{let{globalFilterFn:t}=e.options;return D(t)?t:t===`auto`?e.getGlobalAutoFilterFn():e.options.filterFns?.[t]??B[t]},e.setGlobalFilter=t=>{e.options.onGlobalFilterChange==null||e.options.onGlobalFilterChange(t)},e.resetGlobalFilter=t=>{e.setGlobalFilter(t?void 0:e.initialState.globalFilter)}}},ct={getInitialState:e=>({expanded:{},...e}),getDefaultOptions:e=>({onExpandedChange:E(`expanded`,e),paginateExpandedRows:!0}),createTable:e=>{let t=!1,n=!1;e._autoResetExpanded=()=>{if(!t){e._queue(()=>{t=!0});return}if(e.options.autoResetAll??e.options.autoResetExpanded??!e.options.manualExpanding){if(n)return;n=!0,e._queue(()=>{e.resetExpanded(),n=!1})}},e.setExpanded=t=>e.options.onExpandedChange==null?void 0:e.options.onExpandedChange(t),e.toggleAllRowsExpanded=t=>{t??!e.getIsAllRowsExpanded()?e.setExpanded(!0):e.setExpanded({})},e.resetExpanded=t=>{e.setExpanded(t?{}:e.initialState?.expanded??{})},e.getCanSomeRowsExpand=()=>e.getPrePaginationRowModel().flatRows.some(e=>e.getCanExpand()),e.getToggleAllRowsExpandedHandler=()=>t=>{t.persist==null||t.persist(),e.toggleAllRowsExpanded()},e.getIsSomeRowsExpanded=()=>{let t=e.getState().expanded;return t===!0||Object.values(t).some(Boolean)},e.getIsAllRowsExpanded=()=>{let t=e.getState().expanded;return typeof t==`boolean`?t===!0:!(!Object.keys(t).length||e.getRowModel().flatRows.some(e=>!e.getIsExpanded()))},e.getExpandedDepth=()=>{let t=0;return(e.getState().expanded===!0?Object.keys(e.getRowModel().rowsById):Object.keys(e.getState().expanded)).forEach(e=>{let n=e.split(`.`);t=Math.max(t,n.length)}),t},e.getPreExpandedRowModel=()=>e.getSortedRowModel(),e.getExpandedRowModel=()=>(!e._getExpandedRowModel&&e.options.getExpandedRowModel&&(e._getExpandedRowModel=e.options.getExpandedRowModel(e)),e.options.manualExpanding||!e._getExpandedRowModel?e.getPreExpandedRowModel():e._getExpandedRowModel())},createRow:(e,t)=>{e.toggleExpanded=n=>{t.setExpanded(r=>{let i=r===!0?!0:!!(r!=null&&r[e.id]),a={};if(r===!0?Object.keys(t.getRowModel().rowsById).forEach(e=>{a[e]=!0}):a=r,n??=!i,!i&&n)return{...a,[e.id]:!0};if(i&&!n){let{[e.id]:t,...n}=a;return n}return r})},e.getIsExpanded=()=>{let n=t.getState().expanded;return!!((t.options.getIsRowExpanded==null?void 0:t.options.getIsRowExpanded(e))??(n===!0||n?.[e.id]))},e.getCanExpand=()=>{var n;return(t.options.getRowCanExpand==null?void 0:t.options.getRowCanExpand(e))??((t.options.enableExpanding??!0)&&!!((n=e.subRows)!=null&&n.length))},e.getIsAllParentsExpanded=()=>{let n=!0,r=e;for(;n&&r.parentId;)r=t.getRow(r.parentId,!0),n=r.getIsExpanded();return n},e.getToggleExpandedHandler=()=>{let t=e.getCanExpand();return()=>{t&&e.toggleExpanded()}}}},lt=0,ut=10,dt=()=>({pageIndex:lt,pageSize:ut}),ft={getInitialState:e=>({...e,pagination:{...dt(),...e?.pagination}}),getDefaultOptions:e=>({onPaginationChange:E(`pagination`,e)}),createTable:e=>{let t=!1,n=!1;e._autoResetPageIndex=()=>{if(!t){e._queue(()=>{t=!0});return}if(e.options.autoResetAll??e.options.autoResetPageIndex??!e.options.manualPagination){if(n)return;n=!0,e._queue(()=>{e.resetPageIndex(),n=!1})}},e.setPagination=t=>e.options.onPaginationChange==null?void 0:e.options.onPaginationChange(e=>T(t,e)),e.resetPagination=t=>{e.setPagination(t?dt():e.initialState.pagination??dt())},e.setPageIndex=t=>{e.setPagination(n=>{let r=T(t,n.pageIndex),i=e.options.pageCount===void 0||e.options.pageCount===-1?2**53-1:e.options.pageCount-1;return r=Math.max(0,Math.min(r,i)),{...n,pageIndex:r}})},e.resetPageIndex=t=>{var n;e.setPageIndex(t?lt:((n=e.initialState)==null||(n=n.pagination)==null?void 0:n.pageIndex)??lt)},e.resetPageSize=t=>{var n;e.setPageSize(t?ut:((n=e.initialState)==null||(n=n.pagination)==null?void 0:n.pageSize)??ut)},e.setPageSize=t=>{e.setPagination(e=>{let n=Math.max(1,T(t,e.pageSize)),r=e.pageSize*e.pageIndex,i=Math.floor(r/n);return{...e,pageIndex:i,pageSize:n}})},e.setPageCount=t=>e.setPagination(n=>{let r=T(t,e.options.pageCount??-1);return typeof r==`number`&&(r=Math.max(-1,r)),{...n,pageCount:r}}),e.getPageOptions=O(()=>[e.getPageCount()],e=>{let t=[];return e&&e>0&&(t=[...Array(e)].fill(null).map((e,t)=>t)),t},k(e.options,`debugTable`,`getPageOptions`)),e.getCanPreviousPage=()=>e.getState().pagination.pageIndex>0,e.getCanNextPage=()=>{let{pageIndex:t}=e.getState().pagination,n=e.getPageCount();return n===-1?!0:n===0?!1:t<n-1},e.previousPage=()=>e.setPageIndex(e=>e-1),e.nextPage=()=>e.setPageIndex(e=>e+1),e.firstPage=()=>e.setPageIndex(0),e.lastPage=()=>e.setPageIndex(e.getPageCount()-1),e.getPrePaginationRowModel=()=>e.getExpandedRowModel(),e.getPaginationRowModel=()=>(!e._getPaginationRowModel&&e.options.getPaginationRowModel&&(e._getPaginationRowModel=e.options.getPaginationRowModel(e)),e.options.manualPagination||!e._getPaginationRowModel?e.getPrePaginationRowModel():e._getPaginationRowModel()),e.getPageCount=()=>e.options.pageCount??Math.ceil(e.getRowCount()/e.getState().pagination.pageSize),e.getRowCount=()=>e.options.rowCount??e.getPrePaginationRowModel().rows.length}},pt=()=>({top:[],bottom:[]}),mt={getInitialState:e=>({rowPinning:pt(),...e}),getDefaultOptions:e=>({onRowPinningChange:E(`rowPinning`,e)}),createRow:(e,t)=>{e.pin=(n,r,i)=>{let a=r?e.getLeafRows().map(e=>{let{id:t}=e;return t}):[],o=i?e.getParentRows().map(e=>{let{id:t}=e;return t}):[],s=new Set([...o,e.id,...a]);t.setRowPinning(e=>n===`bottom`?{top:(e?.top??[]).filter(e=>!(s!=null&&s.has(e))),bottom:[...(e?.bottom??[]).filter(e=>!(s!=null&&s.has(e))),...Array.from(s)]}:n===`top`?{top:[...(e?.top??[]).filter(e=>!(s!=null&&s.has(e))),...Array.from(s)],bottom:(e?.bottom??[]).filter(e=>!(s!=null&&s.has(e)))}:{top:(e?.top??[]).filter(e=>!(s!=null&&s.has(e))),bottom:(e?.bottom??[]).filter(e=>!(s!=null&&s.has(e)))})},e.getCanPin=()=>{let{enableRowPinning:n,enablePinning:r}=t.options;return typeof n==`function`?n(e):n??r??!0},e.getIsPinned=()=>{let n=[e.id],{top:r,bottom:i}=t.getState().rowPinning,a=n.some(e=>r?.includes(e)),o=n.some(e=>i?.includes(e));return a?`top`:o?`bottom`:!1},e.getPinnedIndex=()=>{let n=e.getIsPinned();return n?((n===`top`?t.getTopRows():t.getBottomRows())?.map(e=>{let{id:t}=e;return t}))?.indexOf(e.id)??-1:-1}},createTable:e=>{e.setRowPinning=t=>e.options.onRowPinningChange==null?void 0:e.options.onRowPinningChange(t),e.resetRowPinning=t=>e.setRowPinning(t?pt():e.initialState?.rowPinning??pt()),e.getIsSomeRowsPinned=t=>{let n=e.getState().rowPinning;return t?!!n[t]?.length:!!(n.top?.length||n.bottom?.length)},e._getPinnedRows=(t,n,r)=>(e.options.keepPinnedRows??!0?(n??[]).map(t=>{let n=e.getRow(t,!0);return n.getIsAllParentsExpanded()?n:null}):(n??[]).map(e=>t.find(t=>t.id===e))).filter(Boolean).map(e=>({...e,position:r})),e.getTopRows=O(()=>[e.getRowModel().rows,e.getState().rowPinning.top],(t,n)=>e._getPinnedRows(t,n,`top`),k(e.options,`debugRows`,`getTopRows`)),e.getBottomRows=O(()=>[e.getRowModel().rows,e.getState().rowPinning.bottom],(t,n)=>e._getPinnedRows(t,n,`bottom`),k(e.options,`debugRows`,`getBottomRows`)),e.getCenterRows=O(()=>[e.getRowModel().rows,e.getState().rowPinning.top,e.getState().rowPinning.bottom],(e,t,n)=>{let r=new Set([...t??[],...n??[]]);return e.filter(e=>!r.has(e.id))},k(e.options,`debugRows`,`getCenterRows`))}},ht={getInitialState:e=>({rowSelection:{},...e}),getDefaultOptions:e=>({onRowSelectionChange:E(`rowSelection`,e),enableRowSelection:!0,enableMultiRowSelection:!0,enableSubRowSelection:!0}),createTable:e=>{e.setRowSelection=t=>e.options.onRowSelectionChange==null?void 0:e.options.onRowSelectionChange(t),e.resetRowSelection=t=>e.setRowSelection(t?{}:e.initialState.rowSelection??{}),e.toggleAllRowsSelected=t=>{e.setRowSelection(n=>{t=t===void 0?!e.getIsAllRowsSelected():t;let r={...n},i=e.getPreGroupedRowModel().flatRows;return t?i.forEach(e=>{e.getCanSelect()&&(r[e.id]=!0)}):i.forEach(e=>{delete r[e.id]}),r})},e.toggleAllPageRowsSelected=t=>e.setRowSelection(n=>{let r=t===void 0?!e.getIsAllPageRowsSelected():t,i={...n};return e.getRowModel().rows.forEach(t=>{gt(i,t.id,r,!0,e)}),i}),e.getPreSelectedRowModel=()=>e.getCoreRowModel(),e.getSelectedRowModel=O(()=>[e.getState().rowSelection,e.getCoreRowModel()],(t,n)=>Object.keys(t).length?be(e,n):{rows:[],flatRows:[],rowsById:{}},k(e.options,`debugTable`,`getSelectedRowModel`)),e.getFilteredSelectedRowModel=O(()=>[e.getState().rowSelection,e.getFilteredRowModel()],(t,n)=>Object.keys(t).length?be(e,n):{rows:[],flatRows:[],rowsById:{}},k(e.options,`debugTable`,`getFilteredSelectedRowModel`)),e.getGroupedSelectedRowModel=O(()=>[e.getState().rowSelection,e.getSortedRowModel()],(t,n)=>Object.keys(t).length?be(e,n):{rows:[],flatRows:[],rowsById:{}},k(e.options,`debugTable`,`getGroupedSelectedRowModel`)),e.getIsAllRowsSelected=()=>{let t=e.getFilteredRowModel().flatRows,{rowSelection:n}=e.getState(),r=!!(t.length&&Object.keys(n).length);return r&&t.some(e=>e.getCanSelect()&&!n[e.id])&&(r=!1),r},e.getIsAllPageRowsSelected=()=>{let t=e.getPaginationRowModel().flatRows.filter(e=>e.getCanSelect()),{rowSelection:n}=e.getState(),r=!!t.length;return r&&t.some(e=>!n[e.id])&&(r=!1),r},e.getIsSomeRowsSelected=()=>{let t=Object.keys(e.getState().rowSelection??{}).length;return t>0&&t<e.getFilteredRowModel().flatRows.length},e.getIsSomePageRowsSelected=()=>{let t=e.getPaginationRowModel().flatRows;return e.getIsAllPageRowsSelected()?!1:t.filter(e=>e.getCanSelect()).some(e=>e.getIsSelected()||e.getIsSomeSelected())},e.getToggleAllRowsSelectedHandler=()=>t=>{e.toggleAllRowsSelected(t.target.checked)},e.getToggleAllPageRowsSelectedHandler=()=>t=>{e.toggleAllPageRowsSelected(t.target.checked)}},createRow:(e,t)=>{e.toggleSelected=(n,r)=>{let i=e.getIsSelected();t.setRowSelection(a=>{if(n=n===void 0?!i:n,e.getCanSelect()&&i===n)return a;let o={...a};return gt(o,e.id,n,r?.selectChildren??!0,t),o})},e.getIsSelected=()=>{let{rowSelection:n}=t.getState();return xe(e,n)},e.getIsSomeSelected=()=>{let{rowSelection:n}=t.getState();return Se(e,n)===`some`},e.getIsAllSubRowsSelected=()=>{let{rowSelection:n}=t.getState();return Se(e,n)===`all`},e.getCanSelect=()=>typeof t.options.enableRowSelection==`function`?t.options.enableRowSelection(e):t.options.enableRowSelection??!0,e.getCanSelectSubRows=()=>typeof t.options.enableSubRowSelection==`function`?t.options.enableSubRowSelection(e):t.options.enableSubRowSelection??!0,e.getCanMultiSelect=()=>typeof t.options.enableMultiRowSelection==`function`?t.options.enableMultiRowSelection(e):t.options.enableMultiRowSelection??!0,e.getToggleSelectedHandler=()=>{let t=e.getCanSelect();return n=>{t&&e.toggleSelected(n.target?.checked)}}}},gt=(e,t,n,r,i)=>{var a;let o=i.getRow(t,!0);n?(o.getCanMultiSelect()||Object.keys(e).forEach(t=>delete e[t]),o.getCanSelect()&&(e[t]=!0)):delete e[t],r&&(a=o.subRows)!=null&&a.length&&o.getCanSelectSubRows()&&o.subRows.forEach(t=>gt(e,t.id,n,r,i))},_t=/([0-9]+)/gm,vt=(e,t,n)=>we(R(e.getValue(n)).toLowerCase(),R(t.getValue(n)).toLowerCase()),yt=(e,t,n)=>we(R(e.getValue(n)),R(t.getValue(n))),bt=(e,t,n)=>Ce(R(e.getValue(n)).toLowerCase(),R(t.getValue(n)).toLowerCase()),xt=(e,t,n)=>Ce(R(e.getValue(n)),R(t.getValue(n))),St=(e,t,n)=>{let r=e.getValue(n),i=t.getValue(n);return r>i?1:r<i?-1:0},Ct=(e,t,n)=>Ce(e.getValue(n),t.getValue(n)),U={alphanumeric:vt,alphanumericCaseSensitive:yt,text:bt,textCaseSensitive:xt,datetime:St,basic:Ct},wt={getInitialState:e=>({sorting:[],...e}),getDefaultColumnDef:()=>({sortingFn:`auto`,sortUndefined:1}),getDefaultOptions:e=>({onSortingChange:E(`sorting`,e),isMultiSortEvent:e=>e.shiftKey}),createColumn:(e,t)=>{e.getAutoSortingFn=()=>{let n=t.getFilteredRowModel().flatRows.slice(10),r=!1;for(let t of n){let n=t?.getValue(e.id);if(Object.prototype.toString.call(n)===`[object Date]`)return U.datetime;if(typeof n==`string`&&(r=!0,n.split(_t).length>1))return U.alphanumeric}return r?U.text:U.basic},e.getAutoSortDir=()=>typeof t.getFilteredRowModel().flatRows[0]?.getValue(e.id)==`string`?`asc`:`desc`,e.getSortingFn=()=>{if(!e)throw Error();return D(e.columnDef.sortingFn)?e.columnDef.sortingFn:e.columnDef.sortingFn===`auto`?e.getAutoSortingFn():t.options.sortingFns?.[e.columnDef.sortingFn]??U[e.columnDef.sortingFn]},e.toggleSorting=(n,r)=>{let i=e.getNextSortingOrder(),a=n!=null;t.setSorting(o=>{let s=o?.find(t=>t.id===e.id),c=o?.findIndex(t=>t.id===e.id),l=[],u,d=a?n:i===`desc`;return u=o!=null&&o.length&&e.getCanMultiSort()&&r?s?`toggle`:`add`:o!=null&&o.length&&c!==o.length-1?`replace`:s?`toggle`:`replace`,u===`toggle`&&(a||i||(u=`remove`)),u===`add`?(l=[...o,{id:e.id,desc:d}],l.splice(0,l.length-(t.options.maxMultiSortColCount??2**53-1))):l=u===`toggle`?o.map(t=>t.id===e.id?{...t,desc:d}:t):u===`remove`?o.filter(t=>t.id!==e.id):[{id:e.id,desc:d}],l})},e.getFirstSortDir=()=>e.columnDef.sortDescFirst??t.options.sortDescFirst??e.getAutoSortDir()===`desc`?`desc`:`asc`,e.getNextSortingOrder=n=>{let r=e.getFirstSortDir(),i=e.getIsSorted();return i?i!==r&&(t.options.enableSortingRemoval??!0)&&(!n||(t.options.enableMultiRemove??!0))?!1:i===`desc`?`asc`:`desc`:r},e.getCanSort=()=>(e.columnDef.enableSorting??!0)&&(t.options.enableSorting??!0)&&!!e.accessorFn,e.getCanMultiSort=()=>e.columnDef.enableMultiSort??t.options.enableMultiSort??!!e.accessorFn,e.getIsSorted=()=>{let n=t.getState().sorting?.find(t=>t.id===e.id);return n?n.desc?`desc`:`asc`:!1},e.getSortIndex=()=>t.getState().sorting?.findIndex(t=>t.id===e.id)??-1,e.clearSorting=()=>{t.setSorting(t=>t!=null&&t.length?t.filter(t=>t.id!==e.id):[])},e.getToggleSortingHandler=()=>{let n=e.getCanSort();return r=>{n&&(r.persist==null||r.persist(),e.toggleSorting==null||e.toggleSorting(void 0,e.getCanMultiSort()?t.options.isMultiSortEvent==null?void 0:t.options.isMultiSortEvent(r):!1))}}},createTable:e=>{e.setSorting=t=>e.options.onSortingChange==null?void 0:e.options.onSortingChange(t),e.resetSorting=t=>{e.setSorting(t?[]:e.initialState?.sorting??[])},e.getPreSortedRowModel=()=>e.getGroupedRowModel(),e.getSortedRowModel=()=>(!e._getSortedRowModel&&e.options.getSortedRowModel&&(e._getSortedRowModel=e.options.getSortedRowModel(e)),e.options.manualSorting||!e._getSortedRowModel?e.getPreSortedRowModel():e._getSortedRowModel())}},Tt=[Ae,at,et,nt,Me,He,ot,st,wt,$e,ct,ft,mt,ht,it]}));function Dt(){return!0}function Ot(e){return`value`in e?e.value:e}function W(){var e=[...arguments];return new Proxy({get(t){for(let n=e.length-1;n>=0;n--){let r=Ot(e[n])[t];if(r!==void 0)return r}},has(t){for(let n=e.length-1;n>=0;n--)if(t in Ot(e[n]))return!0;return!1},keys(){let t=[];for(let n=0;n<e.length;n++)t.push(...Object.keys(Ot(e[n])));return[...Array.from(new Set(t))]}},Mt)}function kt(e){return W(e,{data:d(e.data)})}function At(e){let t=g(e.data),r=Te(W({state:{},onStateChange:()=>{},renderFallbackValue:null,mergeOptions(e,n){return t?{...e,...n}:W(e,n)}},t?kt(e):e));if(t){let t=f(e.data);oe(t,()=>{r.setState(e=>({...e,data:t.value}))},{immediate:!0})}let i=n(r.initialState);return ie(()=>{r.setOptions(n=>{let r=new Proxy({},{get:(e,t)=>i.value[t]});return W(n,t?kt(e):e,{state:W(r,e.state??{}),onStateChange:t=>{t instanceof Function?i.value=t(i.value):i.value=t,e.onStateChange==null||e.onStateChange(t)}})})}),r}var jt,Mt,Nt=e((()=>{Et(),Et(),i(),jt=Symbol(`merge-proxy`),Mt={get(e,t,n){return t===jt?n:e.get(t)},has(e,t){return e.has(t)},set:Dt,deleteProperty:Dt,getOwnPropertyDescriptor(e,t){return{configurable:!0,enumerable:!0,get(){return e.get(t)},set:Dt,deleteProperty:Dt}},ownKeys(e){return e.keys()}},u({props:[`render`,`props`],setup:e=>()=>typeof e.render==`function`||typeof e.render==`object`?re(e.render,e.props):e.render})})),Pt,Ft,It,Lt,Rt,zt,Bt,Vt,Ht,Ut,Wt,Gt,Kt,G,qt=e((()=>{i(),Nt(),S(),le(),Pt=[`aria-label`],Ft={class:`csp-table`},It={class:`sr-only csp-table__caption`},Lt={class:`csp-table__head`},Rt=[`aria-sort`],zt=[`onClick`],Bt={key:1},Vt={class:`csp-table__body`},Ht={key:0},Ut=[`colspan`],Wt=[`aria-selected`,`onClick`],Gt=[`onClick`],Kt={key:0,class:`csp-table__footer`},G=u({__name:`CspDataTable`,props:t({rows:{},columns:{},rowKey:{},caption:{},selectionMode:{default:`none`},activationMode:{default:`none`},selectedIds:{},selectionLabel:{},size:{default:`md`},pageSize:{},manual:{type:Boolean,default:!1},rowCount:{},emptyLabel:{default:`Aucun résultat`}},{sort:{default:null},sortModifiers:{},page:{default:1},pageModifiers:{}}),emits:t([`toggleRow`,`toggleAll`,`activate`],[`update:sort`,`update:page`]),setup(e,{emit:t}){let n=e,i=t,u=se(e,`sort`),d=se(e,`page`),f=me(),m=h(()=>n.columns.map(e=>f.accessor(t=>e.accessor?.(t)??``,{id:e.id,enableSorting:e.sortable??!1,meta:{align:e.align,width:e.width,label:e.header}}))),g=h(()=>u.value?[u.value]:[]),re=h(()=>n.pageSize??Math.max(n.rows.length,1)),ie=h(()=>({pageIndex:Math.max(0,(d.value??1)-1),pageSize:re.value}));function oe(e,t){return typeof e==`function`?e(t):e}let x=At({get data(){return n.rows},get columns(){return m.value},state:{get sorting(){return g.value},get pagination(){return ie.value}},getRowId:e=>n.rowKey(e),enableMultiSort:!1,manualSorting:n.manual,manualPagination:n.manual,get rowCount(){return n.manual?n.rowCount:void 0},getCoreRowModel:Ee(),getSortedRowModel:ke(),getPaginationRowModel:Oe(),onSortingChange:e=>{let t=oe(e,g.value);u.value=t.length?{id:t[0].id,desc:t[0].desc}:null},onPaginationChange:e=>{d.value=oe(e,ie.value).pageIndex+1}}),ce=h(()=>x.getHeaderGroups()[0]?.headers??[]),le=h(()=>x.getRowModel().rows),S=h(()=>le.value.map(e=>e.id)),fe=h(()=>n.selectionMode===`row`),C=h(()=>n.selectionMode!==`none`),pe=h(()=>n.activationMode===`row`&&!fe.value),w=h(()=>n.activationMode===`cell`),T=h(()=>x.getVisibleLeafColumns().length+ +!!C.value),E=h(()=>!n.selectedIds||S.value.length===0?!1:S.value.every(e=>n.selectedIds.has(e))),D=h(()=>n.selectedIds?!E.value&&S.value.some(e=>n.selectedIds.has(e)):!1),he=h(()=>{let e=n.manual?n.rowCount??0:x.getRowCount(),t=re.value,r=d.value;return{page:r,pageCount:x.getPageCount(),pageSize:t,total:e,canPrevious:x.getCanPreviousPage(),canNext:x.getCanNextPage(),range:e===0?{from:0,to:0}:{from:(r-1)*t+1,to:Math.min(r*t,e)},setPage:e=>x.setPageIndex(e-1),nextPage:()=>x.nextPage(),previousPage:()=>x.previousPage()}});function ge(){i(`toggleAll`,S.value)}function O(e){i(`toggleRow`,e)}function k(e){return e.columnDef.meta?.align}function A(e){return e.columnDef.meta?.width}function j(e){return e.columnDef.meta?.label??e.id}function M(e,t){if(!(!e||e===`start`))return`csp-table__${t}--${e}`}function N(e){let t=e.getIsSorted();return t===`asc`?`ascending`:t===`desc`?`descending`:`none`}function P(e){let t=e.getIsSorted();return t===`asc`?`ri:arrow-up-line`:t===`desc`?`ri:arrow-down-line`:`ri:expand-up-down-line`}function F(e){return n.selectedIds?.has(e.id)??!1}function _e(e){return n.selectionLabel?.(e.original)??`Sélectionner la ligne`}function ve(e){return e==null||e===``?`-`:String(e)}function ye(e){if(fe.value){i(`toggleRow`,e.id);return}pe.value&&i(`activate`,e.id)}function I(e){i(`activate`,e)}return(t,n)=>(y(),s(`div`,{class:r([`csp-table-wrapper`,`csp-table-wrapper--${e.size}`])},[b(`div`,{class:`csp-table__scroll`,tabindex:`0`,role:`region`,"aria-label":e.caption},[b(`table`,Ft,[b(`caption`,It,_(e.caption),1),b(`thead`,Lt,[b(`tr`,null,[C.value?(y(),s(`th`,{key:0,scope:`col`,class:`csp-table__th csp-table__select`,onClick:ge},[b(`div`,{class:`csp-table__checkbox-wrapper`,onClick:n[0]||=p(()=>{},[`stop`])},[o(de,{variant:`checkbox-only`,label:`Tout sélectionner`,"model-value":E.value,indeterminate:D.value,"onUpdate:modelValue":ge},null,8,[`model-value`,`indeterminate`])])])):ee(``,!0),(y(!0),s(a,null,ae(ce.value,e=>(y(),s(`th`,{key:e.id,scope:`col`,class:r([`csp-table__th`,M(k(e.column),`th`)]),"aria-sort":e.column.getCanSort()?N(e.column):void 0,style:c(A(e.column)?{width:A(e.column)}:void 0)},[v(t.$slots,`header-${e.column.id}`,{column:e.column,label:j(e.column),sorted:e.column.getIsSorted(),canSort:e.column.getCanSort(),toggleSort:t=>e.column.getToggleSortingHandler()?.(t)},()=>[e.column.getCanSort()?(y(),s(`button`,{key:0,type:`button`,class:`csp-table__sort`,onClick:t=>e.column.getToggleSortingHandler()?.(t)},[b(`span`,null,_(j(e.column)),1),o(ue,{class:r([`csp-table__sort-icon`,{"csp-table__sort-icon--inactive":!e.column.getIsSorted()}]),name:P(e.column),size:14},null,8,[`class`,`name`])],8,zt)):(y(),s(`span`,Bt,_(j(e.column)),1))],!0)],14,Rt))),128))])]),b(`tbody`,Vt,[le.value.length===0?(y(),s(`tr`,Ht,[b(`td`,{class:`csp-table__empty`,colspan:T.value},[v(t.$slots,`empty`,{},()=>[ne(_(e.emptyLabel),1)],!0)],8,Ut)])):(y(!0),s(a,{key:1},ae(le.value,e=>(y(),s(`tr`,{key:e.id,class:r([`csp-table__row`,{"csp-table__row--selected":F(e),"csp-table__row--selectable":fe.value||pe.value}]),"aria-selected":C.value?F(e):void 0,onClick:t=>ye(e)},[C.value?(y(),s(`td`,{key:0,class:`csp-table__td csp-table__select`,onClick:p(t=>O(e.id),[`stop`])},[b(`div`,{class:`csp-table__checkbox-wrapper`,onClick:n[1]||=p(()=>{},[`stop`])},[o(de,{variant:`checkbox-only`,label:_e(e),"model-value":F(e),"onUpdate:modelValue":()=>O(e.id)},null,8,[`label`,`model-value`,`onUpdate:modelValue`])])],8,Gt)):ee(``,!0),(y(!0),s(a,null,ae(e.getVisibleCells(),n=>(y(),s(`td`,{key:n.id,class:r([`csp-table__td`,M(k(n.column),`td`)]),style:c(A(n.column)?{width:A(n.column)}:void 0)},[v(t.$slots,`cell-${n.column.id}`,{row:e.original,value:n.getValue(),activate:w.value?()=>I(e.id):void 0},()=>[ne(_(ve(n.getValue())),1)],!0)],6))),128))],10,Wt))),128))])])],8,Pt),t.$slots.footer?(y(),s(`div`,Kt,[v(t.$slots,`footer`,te(l(he.value)),void 0,!0)])):ee(``,!0)],2))}})})),Jt=e((()=>{})),K,Yt=e((()=>{qt(),qt(),Jt(),x(),K=ce(G,[[`__scopeId`,`data-v-cda039ba`]]),G.__docgenInfo=Object.assign({displayName:G.name??G.__name},{exportName:`default`,displayName:`CspDataTable`,type:2,props:[{name:`rows`,global:!1,description:``,tags:[],required:!0,type:`unknown[]`,declarations:[],schema:{kind:`array`,type:`unknown[]`}},{name:`columns`,global:!1,description:``,tags:[],required:!0,type:`CspColumnDef<unknown>[]`,declarations:[],schema:{kind:`array`,type:`CspColumnDef<unknown>[]`}},{name:`rowKey`,global:!1,description:``,tags:[],required:!0,type:`(row: unknown) => string`,declarations:[],schema:{kind:`event`,type:`(row: unknown): string`}},{name:`caption`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`selectionMode`,global:!1,description:``,tags:[],required:!1,type:`"none" | "row" | "checkbox"`,declarations:[],schema:{kind:`enum`,type:`"none" | "row" | "checkbox"`,schema:[`"none"`,`"row"`,`"checkbox"`]},default:`"none"`},{name:`activationMode`,global:!1,description:``,tags:[],required:!1,type:`"none" | "row" | "cell"`,declarations:[],schema:{kind:`enum`,type:`"none" | "row" | "cell"`,schema:[`"none"`,`"row"`,`"cell"`]},default:`"none"`},{name:`selectedIds`,global:!1,description:``,tags:[],required:!1,type:`Set<string>`,declarations:[],schema:{kind:`array`,type:`Set<string>`}},{name:`selectionLabel`,global:!1,description:``,tags:[],required:!1,type:`(row: unknown) => string`,declarations:[],schema:{kind:`event`,type:`(row: unknown): string`}},{name:`size`,global:!1,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg"`,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]},default:`"md"`},{name:`pageSize`,global:!1,description:``,tags:[],required:!1,type:`number`,declarations:[],schema:`number`},{name:`manual`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`rowCount`,global:!1,description:``,tags:[],required:!1,type:`number`,declarations:[],schema:`number`},{name:`emptyLabel`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"Aucun r\\u00E9sultat"`},{name:`sort`,global:!1,description:``,tags:[],required:!1,type:`{ id: string; desc: boolean; }`,declarations:[],schema:{kind:`object`,type:`{ id: string; desc: boolean; }`},default:`null`},{name:`page`,global:!1,description:``,tags:[],required:!1,type:`number`,declarations:[],schema:`number`,default:`1`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`toggleRow`,description:``,tags:[],type:`[id: string]`,signature:`(evt: "toggleRow", id: string): void`,declarations:[],schema:[`string`]},{name:`toggleAll`,description:``,tags:[],type:`[visibleIds: string[]]`,signature:`(evt: "toggleAll", visibleIds: string[]): void`,declarations:[],schema:[{kind:`array`,type:`string[]`}]},{name:`activate`,description:``,tags:[],type:`[id: string]`,signature:`(evt: "activate", id: string): void`,declarations:[],schema:[`string`]},{name:`update:page`,description:``,tags:[],type:`[value: number]`,signature:`(evt: "update:page", value: number): void`,declarations:[],schema:[`number`]},{name:`update:sort`,description:``,tags:[],type:`[value: { id: string; desc: boolean; }]`,signature:`(evt: "update:sort", value: { id: string; desc: boolean; }): void`,declarations:[],schema:[{kind:`object`,type:`{ id: string; desc: boolean; }`}]}],slots:[{name:`empty`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`footer`,type:`{ page: number; pageCount: number; pageSize: number; total: number; canPrevious: boolean; canNext: boolean; range: { from: number; to: number; }; setPage: (value: number) => void; nextPage: () => void; previousPage: () => void; }`,description:``,declarations:[],schema:{kind:`object`,type:`{ page: number; pageCount: number; pageSize: number; total: number; canPrevious: boolean; canNext: boolean; range: { from: number; to: number; }; setPage: (value: number) => void; nextPage: () => void; previousPage: () => void; }`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspDataTable/CspDataTable.vue`})}));function Xt(){let e=n(new Set),t=h(()=>e.value.size);function r(t){let n=new Set(e.value);n.has(t)?n.delete(t):n.add(t),e.value=n}function i(t){let n=t.length>0&&t.every(t=>e.value.has(t)),r=new Set(e.value);n?t.forEach(e=>r.delete(e)):t.forEach(e=>r.add(e)),e.value=r}return{count:t,selectedIds:e,toggle:r,toggleVisible:i}}function Zt(e){return()=>({components:{CspDataTable:K,CspTag:w},setup(){return{columns:J,demos:m(e.map(e=>{let t=Xt();return{...e,count:t.count,selectedIds:t.selectedIds,onToggleRow:e=>t.toggle(e),onToggleAll:e=>t.toggleVisible(e)}}))}},template:`
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
    `})}var q,Qt,J,$t,Y,X,en,Z,Q,$,tn;e((()=>{i(),fe(),pe(),Yt(),q=[{id:`1`,libelle:`Alpha`,reference:`REF-001`,categorie:`Catégorie A`,date:`15/02/26`,quantite:24},{id:`2`,libelle:`Bravo`,reference:`REF-002`,categorie:`Catégorie B`,date:`12/02/26`,quantite:18},{id:`3`,libelle:`Charlie`,reference:`REF-003`,categorie:`Catégorie A`,date:`10/02/26`,quantite:31},{id:`4`,libelle:`Delta`,reference:`REF-004`,categorie:`Catégorie C`,date:`08/02/26`,quantite:12},{id:`5`,libelle:`Echo`,reference:`REF-005`,categorie:`Catégorie B`,date:`05/02/26`,quantite:27},{id:`6`,libelle:`Foxtrot`,reference:`REF-006`,categorie:`Catégorie A`,date:`03/02/26`,quantite:9},{id:`7`,libelle:`Golf`,reference:`REF-007`,categorie:`Catégorie C`,date:`01/02/26`,quantite:15},{id:`8`,libelle:`Hotel`,reference:`REF-008`,categorie:`Catégorie B`,date:`29/01/26`,quantite:22}],Qt=q.slice(0,4),J=[{id:`libelle`,header:`Libellé`,sortable:!0,width:`26%`,accessor:e=>e.libelle},{id:`reference`,header:`Référence`,sortable:!0,width:`18%`,accessor:e=>e.reference},{id:`categorie`,header:`Catégorie`,sortable:!0,width:`22%`,accessor:e=>e.categorie},{id:`date`,header:`Date`,sortable:!0,width:`16%`,accessor:e=>e.date},{id:`quantite`,header:`Quantité`,sortable:!0,align:`end`,width:`18%`,accessor:e=>e.quantite}],$t={title:`Compositions/Génériques/CspDataTable`,component:K,tags:[`autodocs`],parameters:{layout:`padded`,controls:{include:[`selectionMode`,`activationMode`,`size`,`pageSize`]},docs:{description:{component:"Table de données générique avec tri, densité, pagination et sélection. Les cellules riches passent par les slots `cell-*`, les en-têtes par `header-*`, et le footer reçoit le contexte de pagination."}}},argTypes:{selectionMode:{control:{type:`radio`},options:[`none`,`checkbox`,`row`],description:`Mode de sélection des lignes : aucun, case à cocher uniquement, ou clic sur toute la ligne.`,table:{defaultValue:{summary:`none`}}},activationMode:{control:{type:`radio`},options:[`none`,`row`,`cell`],description:'Mode d’activation (navigation / ouverture d’un drawer) : aucun, clic sur toute la ligne, ou clic sur une cible précise exposée via le helper `activate` du slot de cellule. `row` est ignoré si `selectionMode="row"`.',table:{defaultValue:{summary:`none`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Densité d’affichage des lignes.`,table:{defaultValue:{summary:`default`}}},pageSize:{control:{type:`number`,min:1,step:1},description:`Nombre de lignes affichées par page.`,table:{defaultValue:{summary:`5`}}}},args:{selectionMode:`row`,size:`md`,pageSize:5},render:e=>({components:{CspDataTable:K,CspPagination:C,CspTag:w},setup(){let t=Xt();return{args:e,columns:J,count:t.count,rows:q,selectedIds:t.selectedIds,onToggleRow:e=>t.toggle(e),onToggleAll:e=>t.toggleVisible(e)}},template:`
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
    `})},Y={name:`Par défaut`},X={name:`Tailles`,render:()=>({components:{CspDataTable:K,CspTag:w},setup(){return{columns:J,rows:Qt,sizes:[`sm`,`md`,`lg`]}},template:`
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
    `}),parameters:{controls:{disable:!0},docs:{description:{story:`Compare rapidement les trois densités supportées par la table.`}}}},en=[{id:`libelle`,header:`Libellé du produit`,sortable:!0,accessor:e=>e.libelle},{id:`reference`,header:`Référence interne`,sortable:!0,accessor:e=>e.reference},{id:`categorie`,header:`Catégorie de classement`,sortable:!0,accessor:e=>e.categorie},{id:`date`,header:`Date de dernière mise à jour`,sortable:!0,accessor:e=>e.date},{id:`quantite`,header:`Quantité en stock`,sortable:!0,align:`end`,accessor:e=>e.quantite}],Z={name:`Débordement (scroll horizontal)`,render:()=>({components:{CspDataTable:K,CspTag:w},setup(){return{columns:en,rows:Qt}},template:`
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
    `}),parameters:{controls:{disable:!0},docs:{description:{story:`Dans un conteneur trop étroit, la zone de contenu défile horizontalement.`}}}},Q={name:`Modes de sélection`,render:Zt([{name:`Aucune sélection`,rows:q.slice(0,5),size:`md`,selectionMode:`none`},{name:`Sélection par checkbox`,rows:q.slice(0,5),size:`md`,selectionMode:`checkbox`},{name:`Sélection par ligne`,rows:q.slice(0,5),size:`md`,selectionMode:`row`},{name:`État vide`,rows:[],size:`md`,selectionMode:`none`,emptyLabel:`Aucun élément`}]),parameters:{controls:{disable:!0},docs:{description:{story:`Compare les trois comportements de sélection attendus : aucun, checkbox uniquement, ou sélection par clic sur toute la ligne.`}}}},$={name:`Modes d’activation`,render:()=>({components:{CspDataTable:K,CspTag:w},setup(){let e=n(null);return{columns:J,rows:q.slice(0,5),lastActivated:e,onActivate:t=>{e.value=t}}},template:`
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
    `}),parameters:{controls:{disable:!0},docs:{description:{story:"Active une ligne (navigation ou ouverture d’un drawer) soit au clic sur toute la ligne (`row`), soit au clic sur une cible précise rendue dans un slot de cellule via le helper `activate` (`cell`). En mode `cell`, le déclencheur reste un vrai bouton focusable au clavier."}}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
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
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
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
}`,...Z.parameters?.docs?.source}}},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
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
}`,...Q.parameters?.docs?.source}}},$.parameters={...$.parameters,docs:{...$.parameters?.docs,source:{originalSource:`{
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
}`,...$.parameters?.docs?.source}}},tn=[`DefaultDemo`,`Sizes`,`Overflow`,`StateVariants`,`ActivationModes`]}))();export{$ as ActivationModes,Y as DefaultDemo,Z as Overflow,X as Sizes,Q as StateVariants,tn as __namedExportsOrder,$t as default};