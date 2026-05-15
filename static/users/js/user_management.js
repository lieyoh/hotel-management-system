/* user_management.js */

function getCookie(name) {
  var match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
  return match ? decodeURIComponent(match[1]) : null;
}

function showToast(message, type) {
  var container = document.getElementById('toast-container');
  if (!container) return;
  var toast = document.createElement('div');
  toast.className = 'toast toast-' + (type || 'success');
  toast.innerHTML = '<span>' + message + '</span>';
  container.appendChild(toast);
  setTimeout(function () {
    toast.classList.add('hide');
    setTimeout(function () { toast.remove(); }, 350);
  }, 3500);
}

function refreshStats() {
  var rows = document.querySelectorAll('#user-table tbody tr[id^="row-"]');
  var active = 0, blocked = 0, staff = 0;
  rows.forEach(function (row) {
    var badge = row.querySelector('.status-badge');
    if (badge) {
      if (badge.classList.contains('badge-active')) active++;
      else blocked++;
    }
    if (row.dataset.isStaff === '1') staff++;
  });
  var elA = document.getElementById('stat-active');
  var elB = document.getElementById('stat-blocked');
  var elS = document.getElementById('stat-staff');
  if (elA) elA.textContent = active;
  if (elB) elB.textContent = blocked;
  if (elS) elS.textContent = staff;
}

function toggleBlock(userId, url) {
  var btn = document.getElementById('btn-' + userId);
  if (!btn) return;

  var originalHTML = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Working...';

  fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'X-Requested-With': 'XMLHttpRequest',
      'Content-Type': 'application/json',
    },
  })
    .then(function (response) {
      if (!response.ok) {
        return response.json().then(function (d) { throw d; });
      }
      return response.json();
    })
    .then(function (data) {
      if (!data.success) {
        showToast(data.message || 'Something went wrong.', 'error');
        btn.disabled = false;
        btn.innerHTML = originalHTML;
        return;
      }

      var isActive = data.is_active;

      /* Update status badge */
      var statusCell = document.getElementById('status-cell-' + userId);
      if (statusCell) {
        statusCell.innerHTML = isActive
          ? '<span class="status-badge badge-active"><span class="status-dot dot-active"></span> Active</span>'
          : '<span class="status-badge badge-inactive"><span class="status-dot dot-inactive"></span> Blocked</span>';
      }

      /* Update avatar */
      var avatar = document.getElementById('avatar-' + userId);
      if (avatar) {
        avatar.style.background = isActive
          ? 'linear-gradient(to bottom right, #60a5fa, #2563eb)'
          : '#d1d5db';
      }

      /* Update button */
      btn.disabled = false;
      if (isActive) {
        btn.className = 'btn-toggle btn-block';
        btn.title = 'Block user';
        btn.innerHTML =
          '<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
          '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" ' +
          'd="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>' +
          '</svg> Block';
      } else {
        btn.className = 'btn-toggle btn-unblock';
        btn.title = 'Unblock user';
        btn.innerHTML =
          '<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
          '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" ' +
          'd="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>' +
          '</svg> Unblock';
      }

      showToast(data.message, 'success');
      refreshStats();
    })
    .catch(function (err) {
      console.error('toggleBlock error:', err);
      btn.disabled = false;
      btn.innerHTML = originalHTML;
      showToast((err && err.message) ? err.message : 'Request failed.', 'error');
    });
}

function filterTable(query) {
  var q = query.toLowerCase().trim();
  var rows = document.querySelectorAll('#user-table tbody tr[id^="row-"]');
  var visible = 0;

  rows.forEach(function (row) {
    var match =
      !q ||
      (row.dataset.username || '').includes(q) ||
      (row.dataset.email    || '').includes(q) ||
      (row.dataset.name     || '').includes(q);
    row.style.display = match ? '' : 'none';
    if (match) visible++;
  });

  var noRow = document.getElementById('no-results-row');
  if (visible === 0 && q) {
    if (!noRow) {
      noRow = document.createElement('tr');
      noRow.id = 'no-results-row';
      noRow.innerHTML =
        '<td colspan="6" class="px-5 py-8 text-center text-gray-400 text-sm">' +
        'No users match "<strong>' + q + '</strong>"</td>';
      document.querySelector('#user-table tbody').appendChild(noRow);
    }
  } else if (noRow) {
    noRow.remove();
  }
}

/* Run on load */
document.addEventListener('DOMContentLoaded', refreshStats);