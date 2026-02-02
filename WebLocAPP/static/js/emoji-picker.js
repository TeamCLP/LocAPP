// Emoji Picker Component for LocApp

// Emoji catalog organized by categories
const EMOJI_CATALOG = {
    'Activités': {
        icon: '🎯',
        emojis: ['🎯', '⛷️', '🏂', '🎿', '🛷', '🏔️', '⛰️', '🗻', '🏕️', '🏖️', '🏜️', '🏞️', '🌊', '🏊', '🚣', '🛶', '🚴', '🚵', '🧗', '🤸', '🏃', '🚶', '🧘', '🎣', '🏇', '⛳', '🎾', '🏀', '⚽', '🎱']
    },
    'Nature': {
        icon: '🌿',
        emojis: ['🌿', '🌲', '🌳', '🌴', '🌵', '🌾', '🌻', '🌺', '🌸', '🌷', '🌹', '🍀', '🍁', '🍂', '🍃', '🌈', '☀️', '🌤️', '⛅', '🌦️', '🌧️', '❄️', '🌨️', '💧', '🔥', '🌙', '⭐', '🦋', '🐝', '🦅']
    },
    'Lieux': {
        icon: '🏛️',
        emojis: ['🏛️', '🏰', '🏯', '🗼', '🗽', '⛪', '🕌', '🕍', '⛩️', '🏠', '🏡', '🏢', '🏣', '🏤', '🏥', '🏦', '🏨', '🏩', '🏪', '🏫', '🏬', '🏭', '🏗️', '🌉', '🌁', '🗿', '⛲', '🎡', '🎢', '🎪']
    },
    'Transport': {
        icon: '🚗',
        emojis: ['🚗', '🚕', '🚙', '🚌', '🚎', '🏎️', '🚓', '🚑', '🚒', '🚐', '🛻', '🚚', '🚛', '🚜', '🛵', '🏍️', '🚲', '🛴', '🚂', '🚃', '🚄', '🚅', '🚆', '🚇', '🚈', '✈️', '🛫', '🛬', '🚁', '⛵']
    },
    'Nourriture': {
        icon: '🍽️',
        emojis: ['🍽️', '🍴', '🥄', '🍕', '🍔', '🍟', '🌭', '🥪', '🌮', '🌯', '🥗', '🥘', '🍝', '🍜', '🍲', '🍛', '🍣', '🍱', '🥟', '🍤', '🍩', '🍪', '🎂', '🍰', '🧁', '🥐', '🥖', '🧀', '🥩', '🍷']
    },
    'Services': {
        icon: '🛎️',
        emojis: ['🛎️', '🏪', '🏬', '🏥', '💊', '🏦', '💰', '🛒', '🧺', '🧹', '🧼', '🪥', '✂️', '💇', '💈', '🔧', '🔨', '🪛', '📦', '📫', '📬', '🏧', '⛽', '🅿️', '🚿', '🛁', '🚽', '🪠', '🧴', '🧽']
    },
    'Urgences': {
        icon: '🆘',
        emojis: ['🆘', '🚨', '🚒', '🚑', '🚓', '👮', '👨‍🚒', '👨‍⚕️', '⚠️', '🔴', '🟠', '🟡', '📞', '☎️', '📱', '🏥', '💉', '🩺', '🩹', '💊', '🔥', '💧', '⚡', '🌊', '🏔️', '❌', '✅', '❗', '❓', '🔔']
    },
    'Maison': {
        icon: '🏠',
        emojis: ['🏠', '🏡', '🛋️', '🛏️', '🚿', '🛁', '🚽', '🪑', '🪞', '🖼️', '📺', '💡', '🔌', '🔑', '🗝️', '🚪', '🪟', '🧹', '🧺', '🧼', '🪥', '🧴', '🛒', '📦', '🎁', '🌡️', '❄️', '🔥', '💨', '☀️']
    },
    'Symboles': {
        icon: '⭐',
        emojis: ['⭐', '🌟', '✨', '💫', '⚡', '🔥', '💧', '❄️', '🌈', '☀️', '🌙', '💯', '✅', '❌', '❓', '❗', '💡', '💰', '💎', '🎯', '🏆', '🥇', '🥈', '🥉', '🎖️', '🏅', '📌', '📍', '🔔', '💬']
    },
    'Drapeaux': {
        icon: '🏳️',
        emojis: ['🇫🇷', '🇪🇺', '🇬🇧', '🇺🇸', '🇩🇪', '🇮🇹', '🇪🇸', '🇵🇹', '🇧🇪', '🇨🇭', '🇦🇹', '🇳🇱', '🇱🇺', '🇲🇨', '🇬🇷', '🇯🇵', '🇨🇳', '🇰🇷', '🇦🇺', '🇨🇦', '🇧🇷', '🇲🇽', '🇦🇷', '🇮🇳', '🇷🇺', '🇹🇷', '🇪🇬', '🇲🇦', '🇿🇦', '🏳️']
    }
};

// Create and manage emoji picker
class EmojiPicker {
    constructor() {
        this.currentInput = null;
        this.pickerElement = null;
        this.isOpen = false;
        this.init();
    }

    init() {
        this.createPickerElement();
        this.addGlobalListeners();
    }

    createPickerElement() {
        // Create picker container
        const picker = document.createElement('div');
        picker.className = 'emoji-picker';
        picker.innerHTML = `
            <div class="emoji-picker-header">
                <span class="emoji-picker-title">Choisir un emoji</span>
                <button type="button" class="emoji-picker-close">&times;</button>
            </div>
            <div class="emoji-picker-categories">
                ${Object.entries(EMOJI_CATALOG).map(([name, cat]) => `
                    <button type="button" class="emoji-category-btn" data-category="${name}" title="${name}">
                        ${cat.icon}
                    </button>
                `).join('')}
            </div>
            <div class="emoji-picker-content">
                <div class="emoji-picker-search">
                    <input type="text" class="emoji-search-input" placeholder="Rechercher...">
                </div>
                <div class="emoji-grid"></div>
            </div>
        `;

        document.body.appendChild(picker);
        this.pickerElement = picker;

        // Add event listeners
        this.addPickerListeners();

        // Show first category by default
        this.showCategory(Object.keys(EMOJI_CATALOG)[0]);
    }

    addPickerListeners() {
        // Close button
        this.pickerElement.querySelector('.emoji-picker-close').addEventListener('click', () => {
            this.close();
        });

        // Category buttons
        this.pickerElement.querySelectorAll('.emoji-category-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.showCategory(e.currentTarget.dataset.category);
                // Update active state
                this.pickerElement.querySelectorAll('.emoji-category-btn').forEach(b => b.classList.remove('active'));
                e.currentTarget.classList.add('active');
            });
        });

        // Search input
        this.pickerElement.querySelector('.emoji-search-input').addEventListener('input', (e) => {
            this.searchEmojis(e.target.value);
        });

        // Emoji grid click (event delegation)
        this.pickerElement.querySelector('.emoji-grid').addEventListener('click', (e) => {
            if (e.target.classList.contains('emoji-item')) {
                this.selectEmoji(e.target.textContent);
            }
        });

        // Set first category as active
        const firstCategoryBtn = this.pickerElement.querySelector('.emoji-category-btn');
        if (firstCategoryBtn) {
            firstCategoryBtn.classList.add('active');
        }
    }

    addGlobalListeners() {
        // Close picker when clicking outside
        document.addEventListener('click', (e) => {
            if (this.isOpen &&
                !this.pickerElement.contains(e.target) &&
                !e.target.classList.contains('emoji-trigger') &&
                !e.target.closest('.emoji-input-wrapper')) {
                this.close();
            }
        });

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }

    showCategory(categoryName) {
        const category = EMOJI_CATALOG[categoryName];
        if (!category) return;

        const grid = this.pickerElement.querySelector('.emoji-grid');
        grid.innerHTML = category.emojis.map(emoji => `
            <button type="button" class="emoji-item" title="${emoji}">${emoji}</button>
        `).join('');

        // Clear search
        this.pickerElement.querySelector('.emoji-search-input').value = '';
    }

    searchEmojis(query) {
        const grid = this.pickerElement.querySelector('.emoji-grid');

        if (!query.trim()) {
            // Show active category
            const activeBtn = this.pickerElement.querySelector('.emoji-category-btn.active');
            if (activeBtn) {
                this.showCategory(activeBtn.dataset.category);
            }
            return;
        }

        // Search in all categories
        const results = [];
        const lowerQuery = query.toLowerCase();

        Object.entries(EMOJI_CATALOG).forEach(([name, cat]) => {
            if (name.toLowerCase().includes(lowerQuery)) {
                results.push(...cat.emojis);
            }
        });

        // If no category match, show all emojis (limited)
        if (results.length === 0) {
            Object.values(EMOJI_CATALOG).forEach(cat => {
                results.push(...cat.emojis);
            });
        }

        // Remove duplicates and limit results
        const uniqueResults = [...new Set(results)].slice(0, 50);

        grid.innerHTML = uniqueResults.map(emoji => `
            <button type="button" class="emoji-item" title="${emoji}">${emoji}</button>
        `).join('');
    }

    selectEmoji(emoji) {
        if (this.currentInput) {
            this.currentInput.value = emoji;
            // Trigger input event for preview updates
            this.currentInput.dispatchEvent(new Event('input', { bubbles: true }));
        }
        this.close();
    }

    open(inputElement, triggerElement) {
        this.currentInput = inputElement;
        this.isOpen = true;

        // Position picker near the trigger
        const rect = triggerElement.getBoundingClientRect();
        const pickerRect = this.pickerElement.getBoundingClientRect();

        let top = rect.bottom + 8;
        let left = rect.left;

        // Check if picker would go off screen
        if (left + 320 > window.innerWidth) {
            left = window.innerWidth - 330;
        }
        if (top + 400 > window.innerHeight) {
            top = rect.top - 408;
        }

        this.pickerElement.style.top = `${top}px`;
        this.pickerElement.style.left = `${left}px`;
        this.pickerElement.classList.add('open');

        // Focus search input
        setTimeout(() => {
            this.pickerElement.querySelector('.emoji-search-input').focus();
        }, 100);
    }

    close() {
        this.isOpen = false;
        this.pickerElement.classList.remove('open');
        this.currentInput = null;
    }
}

// Initialize global emoji picker instance
let emojiPicker = null;

function initEmojiPicker() {
    if (!emojiPicker) {
        emojiPicker = new EmojiPicker();
    }
    return emojiPicker;
}

// Helper function to create emoji input field
function createEmojiInput(inputId, labelText, currentValue = '') {
    return `
        <div class="form-group">
            <label class="form-label" for="${inputId}">${labelText}</label>
            <div class="emoji-input-wrapper">
                <input type="text"
                       class="form-control emoji-input"
                       id="${inputId}"
                       name="${inputId}"
                       value="${currentValue}"
                       readonly
                       placeholder="Cliquez pour choisir">
                <button type="button" class="emoji-trigger" onclick="openEmojiPicker('${inputId}', this)">
                    ${currentValue || '😀'}
                </button>
            </div>
        </div>
    `;
}

// Open emoji picker for a specific input
function openEmojiPicker(inputId, triggerElement) {
    const picker = initEmojiPicker();
    const input = document.getElementById(inputId);
    if (input) {
        picker.open(input, triggerElement);
    }
}

// Update emoji trigger button when input changes
function updateEmojiTrigger(inputId) {
    const input = document.getElementById(inputId);
    const wrapper = input?.closest('.emoji-input-wrapper');
    const trigger = wrapper?.querySelector('.emoji-trigger');
    if (trigger && input.value) {
        trigger.textContent = input.value;
    }
}

// Initialize emoji inputs on page load
document.addEventListener('DOMContentLoaded', function() {
    initEmojiPicker();

    // Add change listener to all emoji inputs
    document.querySelectorAll('.emoji-input').forEach(input => {
        input.addEventListener('input', function() {
            updateEmojiTrigger(this.id);
        });
    });
});
