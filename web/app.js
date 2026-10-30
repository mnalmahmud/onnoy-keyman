(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const editor = $("editor");
  const status = $("status");
  const statusLabel = $("status-label");
  const count = $("count");
  const copy = $("copy");
  const clear = $("clear");
  const inspect = $("inspect");
  const unicodePanel = $("unicode-panel");
  const codepoints = $("codepoints");
  const feedback = $("feedback");
  const keyboard = $("keyboard");
  const details = $("key-details");
  const layerHint = $("layer-hint");
  const errorHelp = $("error-help");
  const errorDetail = $("error-detail");
  const search = $("key-search");
  const searchFeedback = $("search-feedback");
  const layerButtons = [...document.querySelectorAll("[data-layer]")];
  const rows = ["1234567890-=", "QWERTYUIOP[]", "ASDFGHJKL;", "ZXCVBNM.", " "];
  const layerNames = ["Base", "Shift", "AltGr", "AltGr + Shift"];
  const mapKey = (key) => key === " " ? "SPACE" : key;
  const layerHints = [
    "Unmodified keys", "Hold Shift for this layer",
    "Hold Right Alt (AltGr) for this layer", "Hold Shift + Right Alt for this layer"
  ];

  let mapping = null;
  let selectedLayer = 0;
  let visibleLayer = -1;
  let selectedKey = null;
  let shiftDown = false;
  let altGrDown = false;

  function describe(value) {
    if (value === null) return "—";
    if (value === "\u200c") return "ZWNJ";
    if (value === "\u200d") return "ZWJ";
    if (value === "𑷰") return "𑷰"; // Keep actual Unicode; font fallback may show a box.
    return value;
  }

  function updateEditor() {
    const characters = [...editor.value];
    count.textContent = String(characters.length);
    copy.disabled = characters.length === 0;
    if (!unicodePanel.hidden) {
      codepoints.textContent = characters.map((character) =>
        character + " U+" + character.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")
      ).join(" · ") || "Nothing to inspect yet.";
    }
  }

  function showDetails(key) {
    if (!mapping) return;
    details.textContent = key + "  ·  " +
      mapping[mapKey(key)].map((value, index) => layerNames[index] + ": " + describe(value)).join("   |   ");
  }

  function draw(layer) {
    if (!mapping || layer === visibleLayer && keyboard.childElementCount) return;
    visibleLayer = layer;
    const fragment = document.createDocumentFragment();
    for (const rowKeys of rows) {
      const row = document.createElement("div");
      row.className = "keyboard-row";
      for (const key of rowKeys) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "keyboard-key";
        button.dataset.key = key;
        button.classList.toggle("selected", key === selectedKey);
        button.setAttribute("aria-pressed", String(key === selectedKey));
        button.setAttribute("aria-label", key + ": " + layerNames[layer] + " " + describe(mapping[mapKey(key)][layer]));
        const symbol = document.createElement("span");
        symbol.className = "key-symbol";
        symbol.lang = "bn";
        symbol.textContent = key === " " && mapping.SPACE[layer] === " " ? "Space" : describe(mapping[mapKey(key)][layer]);
        if (mapping[mapKey(key)][layer] === null) button.classList.add("unassigned");
        const label = document.createElement("span");
        label.className = "key-label";
        label.textContent = key === " " ? "Space" : key;
        button.append(symbol, label);
        button.addEventListener("click", () => {
          selectedKey = key;
          visibleLayer = -1;
          draw(layer);
          showDetails(key);
        });
        row.append(button);
      }
      fragment.append(row);
    }
    keyboard.replaceChildren(fragment);
    filterKeys();
    layerHint.textContent = layerHints[layer];
    for (const button of layerButtons) {
      const active = Number(button.dataset.layer) === layer;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    }
  }

  function filterKeys() {
    if (!mapping || !search) return;
    const q = search.value.trim().toLocaleLowerCase();
    let matches = 0;
    for (const button of keyboard.querySelectorAll(".keyboard-key")) {
      const key = button.dataset.key;
      const values = mapping[mapKey(key)];
      const hit = !q || (key === " " ? "space" : key).toLowerCase().includes(q) ||
        values.some(value => value && (value.toLocaleLowerCase().includes(q) ||
          [...value].some(ch => ("u+" + ch.codePointAt(0).toString(16)).includes(q.replace(/^u\+/, "u+")))));
      button.classList.toggle("search-match", !!q && hit);
      button.classList.toggle("search-dim", !!q && !hit);
      if (hit) matches++;
    }
    if (searchFeedback) searchFeedback.textContent = q
      ? matches + " matching keys across all four layers" : "Select a key to inspect all four layers";
  }
  if (search) search.addEventListener("input", filterKeys);
  for (const sample of document.querySelectorAll("[data-sample]")) {
    sample.addEventListener("click", () => {
      editor.value = sample.dataset.sample;
      feedback.textContent = "Example inserted";
      updateEditor();
      editor.focus();
      editor.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  }

  function activeLayer() {
    return shiftDown || altGrDown
      ? Number(shiftDown) + Number(altGrDown) * 2
      : selectedLayer;
  }

  for (const button of layerButtons) {
    button.addEventListener("click", () => {
      selectedLayer = Number(button.dataset.layer);
      shiftDown = false;
      altGrDown = false;
      draw(selectedLayer);
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Shift") shiftDown = true;
    if (event.code === "AltRight" || (event.getModifierState && event.getModifierState("AltGraph"))) {
      altGrDown = true;
    }
    draw(activeLayer());
  });
  document.addEventListener("keyup", (event) => {
    if (event.key === "Shift") shiftDown = false;
    if (event.code === "AltRight" || (event.getModifierState && !event.getModifierState("AltGraph"))) {
      altGrDown = false;
    }
    draw(activeLayer());
  });
  window.addEventListener("blur", () => {
    shiftDown = false;
    altGrDown = false;
    draw(selectedLayer);
  });

  inspect.addEventListener("click", () => {
    unicodePanel.hidden = !unicodePanel.hidden;
    inspect.setAttribute("aria-expanded", String(!unicodePanel.hidden));
    updateEditor();
  });
  clear.addEventListener("click", () => {
    editor.value = "";
    feedback.textContent = "";
    updateEditor();
    editor.focus();
  });
  copy.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(editor.value);
      feedback.textContent = "Copied!";
    } catch {
      feedback.textContent = "Copy failed. Select the text to copy manually.";
    }
  });
  editor.addEventListener("input", () => {
    feedback.textContent = "";
    updateEditor();
  });
  updateEditor();

  async function loadLayout() {
    try {
      const response = await fetch("./layout.json");
      if (!response.ok) throw new Error("HTTP " + response.status);
      const layout = await response.json();
      // Display the unchanged hyphen key to preserve the physical number-row spacing.
      const displayed = { ...layout.keys, "-": ["-", "_", null, null] };
      if (!layout.keys || [...rows.join("")].some((key) =>
        !Array.isArray(displayed[mapKey(key)]) || displayed[mapKey(key)].length !== 4
      )) throw new Error("Invalid keyboard mapping");
      mapping = displayed;
      draw(selectedLayer);
    } catch (error) {
      keyboard.textContent = "The key reference could not be loaded.";
      details.textContent = "Check that layout.json was included in the site deployment.";
      console.error("Onnoy key reference:", error);
    }
  }

  async function startKeyboard() {
    try {
      if (!window.keyman) throw new Error("The KeymanWeb engine did not load");
      const km = window.keyman;
      await km.init({ attachType: "manual", ui: "float", setActiveOnRegister: false });
      km.attachToControl(editor);
      await km.addKeyboards({
        id: "onnoy",
        name: "Onnoy (অন্বয়)",
        filename: "./onnoy.js",
        version: "1.0",
        languages: [{ id: "bn", name: "Bangla" }]
      });
      await km.setActiveKeyboard("onnoy", "bn");
      status.classList.remove("loading", "error");
      status.classList.add("ready");
      statusLabel.textContent = "Keyboard ready";
    } catch (error) {
      status.classList.remove("loading", "ready");
      status.classList.add("error");
      statusLabel.textContent = "Keyboard unavailable";
      errorHelp.hidden = false;
      errorDetail.textContent = String(error.message || error);
      console.error("Onnoy KeymanWeb:", error);
    }
  }

  // The reference works even if KeymanWeb fails; ordinary typing stays possible.
  void loadLayout();
  void startKeyboard();
})();
