export default function ({ store, redirect }) {
  if (!store.getters['auth']) {
    redirect('/login')
  }
}
