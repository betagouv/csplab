import { readFileSync } from 'node:fs'
import { dirname } from 'node:path'

const { PR_INDEX, MAIN_INDEX, CHANGED_FILES, PREVIEW_URL, MAIN_URL } = process.env

const FRONTEND_ROOT = 'src/web/'
const SOURCE_ROOT = `${FRONTEND_ROOT}frontend/src/`

function readIndex(path) {
  return Object.values(JSON.parse(readFileSync(path, 'utf8')).entries)
    .filter(entry => entry.type === 'story' || entry.importPath.endsWith('.mdx'))
    .map(entry => ({ ...entry, file: FRONTEND_ROOT + entry.importPath.replace(/^\.\//, '') }))
}

function groupByTitle(entries) {
  const groups = new Map()
  for (const entry of entries) {
    if (!groups.has(entry.title)) groups.set(entry.title, [])
    groups.get(entry.title).push(entry)
  }
  return groups
}

// story titles, names and file names come from the pull request: keep them inert in the comment
function text(value) {
  return String(value).replace(/[\\`*_{}[\]()#+\-!<>|~]/g, '\\$&')
}

function link(baseUrl, entry) {
  const id = encodeURIComponent(entry.id).replace(/[()]/g, char => `%${char.charCodeAt(0).toString(16)}`)
  return `${baseUrl}?path=/${entry.type}/${id}`
}

function entryLinks(entries, baseUrl) {
  return entries.map(entry => `[${text(entry.name)}](${link(baseUrl, entry)})`).join(' · ')
}

const changedFiles = readFileSync(CHANGED_FILES, 'utf8').split('\n').filter(Boolean)
const changedDirs = new Set(changedFiles.map(dirname))
const touches = entry => changedFiles.includes(entry.file) || changedDirs.has(dirname(entry.file))

const prGroups = groupByTitle(readIndex(PR_INDEX))
const mainGroups = groupByTitle(readIndex(MAIN_INDEX))

const added = []
const modified = []
const removed = []
const coveredFiles = new Set()

for (const [title, entries] of prGroups) {
  const mainEntries = mainGroups.get(title)
  const touched = entries.some(touches)
  if (touched) for (const entry of entries) coveredFiles.add(entry.file)
  if (!mainEntries) {
    added.push(`- ${text(title)} : ${entryLinks(entries, PREVIEW_URL)}`)
  }
  else if (touched) {
    const mainIds = new Set(mainEntries.map(entry => entry.id))
    const names = entries
      .map(entry => `[${text(entry.name)}](${link(PREVIEW_URL, entry)})${mainIds.has(entry.id) ? '' : ' (nouvelle)'}`)
      .join(' · ')
    modified.push(`- ${text(title)} : ${names} · [version main](${link(MAIN_URL, mainEntries[0])})`)
  }
}

for (const [title, entries] of mainGroups) {
  if (!prGroups.has(title)) removed.push(`- ${text(title)} : ${entryLinks(entries, MAIN_URL)}`)
}

const coveredDirs = new Set([...coveredFiles].map(dirname))
const orphans = changedFiles.filter(file => file.startsWith(SOURCE_ROOT) && !coveredDirs.has(dirname(file)))

const sections = [
  ['Stories nouvelles', added],
  ['Stories modifiées', modified],
  ['Stories supprimées', removed],
  ['Fichiers modifiés sans story associée', orphans.map(file => `- ${text(file.slice(SOURCE_ROOT.length))}`)],
].filter(([, lines]) => lines.length)

const body = [`📖 Storybook de prévisualisation : ${PREVIEW_URL}`]
if (sections.length) {
  for (const [heading, lines] of sections) body.push(`**${heading}**`, lines.join('\n'))
}
else {
  body.push('Aucune story touchée par les fichiers de cette PR.')
}

process.stdout.write(`${body.join('\n\n')}\n`)
