<template>
  <div>
    <header class="header">
      <nav
        class="navbar header has-shadow has-text-weight-medium"
        role="navigation"
        aria-label="main navigation"
      >
        <div v-for="(item, key) of routes" class="navbar-brand">

          <nuxt-link
            class="navbar-item"
            :to="item.to"
            :key="key"
            exact
          >{{ item.title }}
            <b-icon
              :icon="item.icon"/>
          </nuxt-link>
        </div>
      </nav>
      <div class="user-info">
        Username
        <b-icon icon="bell-outline"/>
      </div>

    </header>

    <section class="content">
      <Sidebar/>
      <div class="main has-shadow">
        <nuxt/>
      </div>
    </section>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";

export default {
  name: 'DefaultLayout',
  components: {
    Sidebar
  },
  data() {
    return {
      routes: [
        {
          title: '',
          icon: 'egg-outline',
          to: {name: 'index'}
        },
        {
          title: 'БД продавцы',
          to: {name: 'sellers'}
        },
        {
          title: 'БД покупатели',
          to: {name: 'buyers'}
        },
        {
          title: 'БД логист',
          to: {name: 'logistic'}
        },
        {
          title: 'Документы',
          to: {name: 'documents'}
        },
        {
          title: 'Статистика',
          to: {name: 'statistics'}
        },
      ]
    }
  }
}
</script>
<style lang="scss" scoped>

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  padding: 0 20px;
}

.content {
  padding: 15px;
  display: grid;
  gap: 15px;
  grid-template-columns:  minmax(auto, 300px) 1fr;
  min-height: 50vh;
}

.user-info {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.main {
  background: #ffffff;
  border: 1px solid #f5f5f5;
  border-radius: 5px;
  padding: 10px;
}

.nuxt-link-active {
  color: blueviolet;
  border-bottom: 2px solid blueviolet;
}
</style>
