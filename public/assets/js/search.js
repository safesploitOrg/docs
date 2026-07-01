const SEARCH_INDEX_PATH = "search-index.json";
const MIN_QUERY_LENGTH = 2;
const MAX_RESULTS = 20;

const searchInput = document.getElementById("searchInput");
const clearSearchButton = document.getElementById("clearSearch");
const resultsContainer = document.getElementById("resultsContainer");
const resultCount = document.getElementById("resultCount");
const searchStatus = document.getElementById("searchStatus");

let searchIndex = [];

function normaliseText(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/\s+/g, " ")
    .trim();
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function tokeniseQuery(query) {
  return normaliseText(query)
    .split(" ")
    .filter((token) => token.length >= MIN_QUERY_LENGTH);
}

function calculateScore(item, tokens) {
  const title = normaliseText(item.title);
  const path = normaliseText(item.path);
  const tags = normaliseText((item.tags || []).join(" "));
  const content = normaliseText(item.content);

  let score = 0;

  for (const token of tokens) {
    if (title.includes(token)) {
      score += 10;
    }

    if (tags.includes(token)) {
      score += 7;
    }

    if (path.includes(token)) {
      score += 4;
    }

    if (content.includes(token)) {
      score += 2;
    }
  }

  return score;
}

function createSnippet(content, tokens) {
  const plainContent = String(content || "").replace(/\s+/g, " ").trim();

  if (!plainContent) {
    return "No preview available.";
  }

  const lowerContent = plainContent.toLowerCase();

  let firstMatchIndex = -1;

  for (const token of tokens) {
    const index = lowerContent.indexOf(token);

    if (index !== -1 && (firstMatchIndex === -1 || index < firstMatchIndex)) {
      firstMatchIndex = index;
    }
  }

  const snippetStart = Math.max(0, firstMatchIndex - 90);
  const snippetEnd = Math.min(plainContent.length, snippetStart + 240);

  let snippet = plainContent.slice(snippetStart, snippetEnd);

  if (snippetStart > 0) {
    snippet = `...${snippet}`;
  }

  if (snippetEnd < plainContent.length) {
    snippet = `${snippet}...`;
  }

  return highlightTokens(escapeHtml(snippet), tokens);
}

function highlightTokens(value, tokens) {
  let highlighted = value;

  for (const token of tokens) {
    const safeToken = token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(`(${safeToken})`, "gi");

    highlighted = highlighted.replace(regex, "<mark>$1</mark>");
  }

  return highlighted;
}

function renderEmptyState(message) {
  resultsContainer.innerHTML = `
    <article class="empty-state">
      <h3>No results</h3>
      <p>${escapeHtml(message)}</p>
    </article>
  `;
}

function renderResults(results, tokens) {
  if (results.length === 0) {
    resultCount.textContent = "0 results";
    renderEmptyState("No matching documents found.");
    return;
  }

  resultCount.textContent = `${results.length} result${results.length === 1 ? "" : "s"}`;

  resultsContainer.innerHTML = results
    .map((result) => {
      const item = result.item;
      const tags = Array.isArray(item.tags) ? item.tags : [];

      const tagHtml = tags
        .map((tag) => `<span class="badge">${escapeHtml(tag)}</span>`)
        .join("");

      return `
        <article class="result-card">
          <h3>
            <a href="${escapeHtml(item.url)}">
              ${escapeHtml(item.title)}
            </a>
          </h3>

          <p>${createSnippet(item.content, tokens)}</p>

          <div class="result-meta">
            <span class="badge">Score ${result.score}</span>
            <span class="badge">${escapeHtml(item.path || "unknown path")}</span>
            ${tagHtml}
          </div>
        </article>
      `;
    })
    .join("");
}

function renderInitialState() {
  resultCount.textContent = "No query entered yet.";
  resultsContainer.innerHTML = `
    <article class="empty-state">
      <h3>Start searching</h3>
      <p>
        Try searching for terms such as <strong>dnsmasq</strong>,
        <strong>GitOps</strong>, <strong>REDCap</strong>,
        <strong>NetApp</strong>, <strong>Linux</strong> or
        <strong>Ansible</strong>.
      </p>
    </article>
  `;
}

function runSearch() {
  const query = searchInput.value;
  const tokens = tokeniseQuery(query);

  if (tokens.length === 0) {
    renderInitialState();
    return;
  }

  const results = searchIndex
    .map((item) => ({
      item,
      score: calculateScore(item, tokens),
    }))
    .filter((result) => result.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, MAX_RESULTS);

  renderResults(results, tokens);
}

async function loadSearchIndex() {
  try {
    const response = await fetch(SEARCH_INDEX_PATH, {
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(`Search index request failed with status ${response.status}`);
    }

    searchIndex = await response.json();

    if (!Array.isArray(searchIndex)) {
      throw new Error("Search index is not an array.");
    }

    searchStatus.textContent = `Search index loaded. ${searchIndex.length} documents indexed.`;
  } catch (error) {
    console.error(error);
    searchStatus.textContent = "Search index could not be loaded.";
    renderEmptyState(
      "The search index is missing. Generate public/search-index.json before deploying."
    );
  }
}

function main() {
  loadSearchIndex();

  searchInput.addEventListener("input", runSearch);

  clearSearchButton.addEventListener("click", () => {
    searchInput.value = "";
    searchInput.focus();
    runSearch();
  });
}

main();
