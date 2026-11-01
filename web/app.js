(() => {
  "use strict";

  const byId = (id) => document.getElementById(id);
  const editor = byId("editor");
  const keyboard = byId("keyboard");
  const details = byId("key-details");
  const status = byId("status");
  const statusLabel = byId("status-label");
  const errorHelp = byId("error-help");
  const errorDetail = byId("error-detail");
  const feedback = byId("feedback");
  const copyButton = byId("copy");
  const clearButton = byId("clear");
  const inspectButton = byId("inspect");
  const unicodePanel = byId("unicode-panel");
  const codepoints = byId("codepoints");
  const count = byId("count");
  const themeControl = byId("theme");
  const geometryControl = byId("geometry");
  const layerHint = byId("layer-hint");
  const modifierIndicator = byId("modifier-indicator");
  const layerButtons = [...document.querySelectorAll("[data-layer]")];

  const layerNames = ["Base", "Shift", "AltGr", "Shift + AltGr"];
  const backtick = String.fromCharCode(96);
  const keyCodes = {
    [backtick]: "Backquote", "-": "Minus", "=": "Equal",
    "[": "BracketLeft", "]": "BracketRight", "\\": "Backslash",
    ";": "Semicolon", "'": "Quote", ",": "Comma",
    ".": "Period", "/": "Slash", "§": "IntlBackslash", " ": "Space"
  };
  const physicalCode = (key) => {
    if (/^[A-Z]$/.test(key)) return "Key" + key;
    if (/^[0-9]$/.test(key)) return "Digit" + key;
    return keyCodes[key];
  };
  const rowsFor = () => {
    const iso = geometryControl.value === "iso";
    return [
      backtick + "1234567890-=",
      "QWERTYUIOP[]" + (iso ? "" : "\\"),
      "ASDFGHJKL;'" + (iso ? "\\" : ""),
      (iso ? "§" : "") + "ZXCVBNM,./",
      " "
    ];
  };

  let mapping = null;
  let keymanReady = false;
  let selectedLayer = 0;
  let selectedKey = null;
  let displayedLayer = -1;
  let displayedGeometry = "";
  let shiftDown = false;
  let altGrDown = false;

  // The keymap only visualizes characters. KeymanWeb owns actual typing.
  function readable(value) {
    if (value === null || value === undefined) return "—";
    if (value === "\u200d") return "ZWJ";
    if (value === "\u200c") return "ZWNJ";
    if (value === " ") return "Space";
    return value;
  }

  function activeLayer() {
    return shiftDown || altGrDown
      ? Number(shiftDown) + Number(altGrDown) * 2
      : selectedLayer;
  }

  function displayError(message) {
    status.classList.remove("ready");
    status.classList.add("error");
    statusLabel.textContent = "Preview unavailable";
    errorHelp.hidden = false;
    errorDetail.textContent = String(message);
  }

  function displayStatus() {
    if (status.classList.contains("error")) return;
    if (mapping && keymanReady) {
      status.classList.add("ready");
      statusLabel.textContent = "KeymanWeb ready";
    } else if (mapping) {
      statusLabel.textContent = "Keymap ready · Connecting keyboard…";
    } else if (keymanReady) {
      statusLabel.textContent = "Keyboard ready · Loading keymap…";
    }
  }

  function showDetails(key) {
    if (!mapping || !key) return;
    const values = mapping[physicalCode(key)];
    if (!values) return;
    details.replaceChildren();
    const title = document.createElement("strong");
    title.textContent = key === " " ? "Space" : key === "§" ? "ISO extra key" : key;
    const description = document.createElement("span");
    description.textContent = "  ·  " + values.map((value, index) =>
      layerNames[index] + ": " + readable(value)).join("   |   ");
    details.append(title, description);
  }

  function drawKeyboard() {
    const layer = activeLayer();
    const geometry = geometryControl.value;
    if (!mapping) return;

    layerHint.textContent = shiftDown || altGrDown
      ? "Physical modifier held · Visual layer updates as you type"
      : "Select a layer above or hold Shift / Right Alt to preview";
    modifierIndicator.textContent = layerNames[layer].toUpperCase();

    for (const button of layerButtons) {
      const active = Number(button.dataset.layer) === layer;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    }
    if (layer === displayedLayer && geometry === displayedGeometry && keyboard.querySelector(".keyboard-key")) {
      return;
    }
    displayedLayer = layer;
    displayedGeometry = geometry;
    const fragment = document.createDocumentFragment();

    for (const rowKeys of rowsFor()) {
      const row = document.createElement("div");
      row.className = "keyboard-row";
      for (const key of rowKeys) {
        const output = mapping[physicalCode(key)]?.[layer];
        const button = document.createElement("button");
        button.type = "button";
        button.className = "keyboard-key";
        button.dataset.key = key;
        button.classList.toggle("selected", selectedKey === key);
        button.classList.toggle("unassigned", output === null || output === undefined);
        button.setAttribute("aria-pressed", String(selectedKey === key));
        button.setAttribute("aria-label", (key === "§" ? "ISO extra key" : key === " " ? "Space" : key) + ", " +
          layerNames[layer] + ": " + readable(output));

        const glyph = document.createElement("span");
        glyph.className = "key-output";
        if (output === "\u200c" || output === "\u200d") glyph.classList.add("key-joiner");
        glyph.lang = output === "\u200c" || output === "\u200d" ? "en" : "bn";
        glyph.textContent = readable(output);

        const caption = document.createElement("span");
        caption.className = "key-label";
        caption.textContent = key === " " ? "SPACE" : key === "§" ? "ISO" : key;
        button.append(glyph, caption);
        button.addEventListener("click", () => {
          selectedKey = key;
          for (const existing of keyboard.querySelectorAll(".keyboard-key")) {
            const current = existing.dataset.key === selectedKey;
            existing.classList.toggle("selected", current);
            existing.setAttribute("aria-pressed", String(current));
          }
          showDetails(key);
        });
        row.append(button);
      }
      fragment.append(row);
    }
    keyboard.replaceChildren(fragment);
    showDetails(selectedKey);
  }

  for (const button of layerButtons) {
    button.addEventListener("click", () => {
      selectedLayer = Number(button.dataset.layer);
      // An explicit preview selection always wins, even after an OS has
      // swallowed a modifier keyup while the editor was focused.
      shiftDown = false;
      altGrDown = false;
      displayedLayer = -1;
      drawKeyboard();
    });
  }

  geometryControl.addEventListener("change", () => {
    selectedKey = null;
    displayedGeometry = "";
    drawKeyboard();
    details.textContent = "Select a key to inspect all four outputs.";
  });

  function modifierState(event, down) {
    const wasShift = shiftDown;
    const wasAltGr = altGrDown;
    const graph = typeof event.getModifierState === "function" &&
      event.getModifierState("AltGraph");
    if (event.key === "Shift" || event.code === "ShiftLeft" || event.code === "ShiftRight") {
      shiftDown = down;
    } else {
      shiftDown = !!event.shiftKey;
    }
    if (event.code === "AltRight" || event.key === "AltGraph") {
      altGrDown = down;
    } else {
      altGrDown = !!graph || (altGrDown && event.altKey);
    }
    if (shiftDown !== wasShift || altGrDown !== wasAltGr) drawKeyboard();
  }

  // KeymanWeb may stop keyboard events while the editor has focus.
  // Capture on window so modifiers update before Keyman processes typing.
  window.addEventListener("keydown", (event) => modifierState(event, true), true);
  window.addEventListener("keyup", (event) => modifierState(event, false), true);
  window.addEventListener("blur", () => {
    shiftDown = false;
    altGrDown = false;
    drawKeyboard();
  });

  // System is the default. Explicit theme choices persist across visits.
  const themeValues = new Set(["system", "light", "dark"]);
  function applyTheme(value) {
    const chosen = themeValues.has(value) ? value : "system";
    themeControl.value = chosen;
    if (chosen === "system") {
      document.documentElement.removeAttribute("data-theme");
    } else {
      document.documentElement.dataset.theme = chosen;
    }
    const prefersDark = window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;
    const dark = chosen === "dark" || (chosen === "system" && prefersDark);
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = dark ? "#171d1b" : "#f7f6f2";
  }
  let savedTheme = "system";
  try {
    savedTheme = window.localStorage.getItem("onnoy-theme") || "system";
  } catch {
    // Private browsing can disable localStorage; System still works.
  }
  applyTheme(savedTheme);
  themeControl.addEventListener("change", () => {
    applyTheme(themeControl.value);
    try {
      if (themeControl.value === "system") {
        window.localStorage.removeItem("onnoy-theme");
      } else {
        window.localStorage.setItem("onnoy-theme", themeControl.value);
      }
    } catch { /* preference applies to this visit */ }
  });
  if (window.matchMedia) {
    const media = window.matchMedia("(prefers-color-scheme: dark)");
    if (media.addEventListener) {
      media.addEventListener("change", () => {
        if (themeControl.value === "system") applyTheme("system");
      });
    }
  }

  const segmenter = typeof Intl.Segmenter === "function"
    ? new Intl.Segmenter("bn", { granularity: "grapheme" }) : null;
  function updateEditor() {
    const chars = [...editor.value];
    const graphemes = segmenter ? [...segmenter.segment(editor.value)].length : chars.length;
    count.textContent = chars.length + " code points · " + graphemes + " graphemes";
    copyButton.disabled = chars.length === 0;
    if (!unicodePanel.hidden) {
      codepoints.replaceChildren();
      if (!chars.length) {
        codepoints.textContent = "Nothing to inspect yet.";
      } else {
        for (const char of chars) {
          const part = document.createElement("span");
          part.textContent = readable(char) + " U+" +
            char.codePointAt(0).toString(16).toUpperCase().padStart(4, "0");
          codepoints.append(part);
        }
      }
    }
  }
  editor.addEventListener("input", () => {
    feedback.textContent = "";
    updateEditor();
  });
  inspectButton.addEventListener("click", () => {
    unicodePanel.hidden = !unicodePanel.hidden;
    inspectButton.setAttribute("aria-expanded", String(!unicodePanel.hidden));
    updateEditor();
  });
  clearButton.addEventListener("click", () => {
    editor.value = "";
    feedback.textContent = "";
    updateEditor();
    editor.focus();
  });
  copyButton.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(editor.value);
      feedback.textContent = "Copied!";
    } catch {
      feedback.textContent = "Copy unavailable — select your text manually.";
    }
  });
  for (const button of document.querySelectorAll("[data-sample]")) {
    button.addEventListener("click", () => {
      editor.value = button.dataset.sample || "";
      feedback.textContent = "Example inserted";
      updateEditor();
      editor.focus();
    });
  }
  updateEditor();

  async function loadLayout() {
    try {
      const response = await fetch("./layout.json");
      if (!response.ok) throw new Error("Unable to fetch generated keymap (HTTP " + response.status + ")");
      const layout = await response.json();
      if (!layout.keys || rowsFor().some((row) => [...row].some((key) => {
        const values = layout.keys[physicalCode(key)];
        return !Array.isArray(values) || values.length !== 4;
      }))) {
        throw new Error("Invalid four-layer keymap");
      }
      mapping = layout.keys;
      drawKeyboard();
      displayStatus();
    } catch (error) {
      keyboard.textContent = "Could not load the Onnoy keyboard reference.";
      displayError(error.message || error);
    }
  }

  async function startKeyman() {
    try {
      const engine = window.keyman;
      if (!engine || typeof engine.init !== "function") {
        throw new Error("KeymanWeb failed to load");
      }
      await engine.init({ attachType: "auto" });
      await engine.addKeyboards({
        id: "onnoy",
        name: "Onnoy",
        language: { id: "bn", name: "Bengali" },
        filename: "./onnoy.js"
      });
      await engine.setActiveKeyboard("onnoy", "bn");
      // Desktop already has our own visual keyboard. Disable KeymanWeb's
      // separate floating OSK so it cannot cover the editor or page.
      // Keep the touch OSK available on phones and tablets.
      if (window.matchMedia("(hover: hover) and (pointer: fine)").matches &&
          engine.osk && typeof engine.osk.hide === "function") {
        engine.osk.hide();
      }
      keymanReady = true;
      displayStatus();
    } catch (error) {
      displayError(error.message || error);
    }
  }

  void loadLayout();
  // The app script runs before KeymanWeb so capture listeners are installed
  // first. Initialize the engine after both deferred scripts have loaded.
  window.addEventListener("load", () => { void startKeyman(); }, { once: true });
})();
