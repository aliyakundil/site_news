//window.addEventListener('scroll', () => {
//    const documentRect = document.documentElement.getBoundingClientRect();
//    console.log('top', documentRect,top);
//    console.log('bottom', documentRect.bottom);
//})


function checkPosition() {
  // Нам потребуется знать высоту документа и высоту экрана:
  const height = document.body.offsetHeight
  const screenHeight = window.innerHeight

  // Они могут отличаться: если на странице много контента,
  // высота документа будет больше высоты экрана (отсюда и скролл).

  // Записываем, сколько пикселей пользователь уже проскроллил:
  const scrolled = window.scrollY

  // Обозначим порог, по приближении к которому
  // будем вызывать какое-то действие.
  // В нашем случае — четверть экрана до конца страницы:
  const threshold = height - screenHeight / 4

  // Отслеживаем, где находится низ экрана относительно страницы:
  const position = scrolled + screenHeight

  if (position >= threshold) {
    // Если мы пересекли полосу-порог, вызываем нужное действие.
  }
};(() => {
  window.addEventListener('scroll', checkPosition)
  window.addEventListener('resize', checkPosition)
})()

function throttle(callee, timeout) {
  let timer = null

  return function perform(...args) {
    if (timer) return

    timer = setTimeout(() => {
      callee(...args)

      clearTimeout(timer)
      timer = null
    }, timeout)
  }
}

;(() => {
  window.addEventListener('scroll', throttle(checkPosition, 3))
  window.addEventListener('resize', throttle(checkPosition, 3))
})()

async function fetchPosts() {
  const { posts, next } = await server.posts(nextPage)
  // Делаем что-то с posts и next.
}

async function checkPosition() {
  // ...Старый код.

  if (position >= threshold) {
    await fetchPosts()
  }
}


