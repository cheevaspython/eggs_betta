<template>
  <aside class="sidebar has-shadow ">

    <b-dropdown
      v-model="selectedOptions"
      :triggers="['hover']"
      multiple
      aria-role="list">
      <template #trigger>
        <div class="sidebar__title">
          <b-icon icon="menu-open"/>
          Активные сущности
        </div>
      </template>

      <b-dropdown-item v-for="option of options"
                       :key="option.value"
                       :value="option.value"
                       aria-role="listitem">
        <span>{{ option.title }}</span>
      </b-dropdown-item>

    </b-dropdown>

    <div v-if="activeTasks" class="container is-fullwidth">
      <div v-for="task in activeTasks" class="sidebar__item" @click="onItemClick(task)">
        <pre>{{task}}</pre>
<!--        <div class="sidebar__row has-text-weight-medium">ID просчета: {{task.id}}</div>-->
<!--        <div class="sidebar__row">Покупатель: <span class="has-text-weight-medium">{{task.buyer_app_detail.buyer_eggs_detail.inn}}</span>  {{task.buyer_app_detail.buyer_eggs_detail.name}}</div>-->
<!--        <div class="sidebar__row">Продавец:  <span class="has-text-weight-medium">{{task.seller_app_detail.seller_eggs_detail.inn}}</span> {{task.seller_app_detail.seller_eggs_detail.name}}</div>-->



<!--        ID:<strong>{{seller.buyer_eggs_detail.inn}} </strong>-->
<!--        {{seller.buyer_eggs_detail.name}}-->
      </div>
    </div>
  </aside>
</template>

<script>
export default {
  name: "Sidebar",
  data() {
    return {
      selectedOptions: [],
      activeTasks: {},
      calculateTasks:[],
      options: [
        {
          value: 'opt1',
          title: 'Все'
        },
        {
          value: 'opt2',
          title: 'Заявки от продавца'
        },
        {
          value: 'opt3',
          title: 'Заявки от покупателя'
        },
        {
          value: 'opt4',
          title: 'Просчеты'
        },
        {
          value: 'opt5',
          title: 'Заявки'
        },
        {
          value: 'opt6',
          title: 'Сделки'
        },
        {
          value: 'opt7',
          title: 'Мои заявки'
        },
      ]
    }
  },
  methods: {
    onItemClick(task) {
      console.log('####### activetask ', task)
      this.$store.dispatch('eggs/setCurrentTask', task)
      this.$router.push('/')
    }
  },
  async created() {
    this.activeTasks = await this.$store.dispatch('bid/getActiveTasks')
    // this.calculateTasks = await this.$store.dispatch('eggs/getCalculateTasks')
    console.log('####### calculateTasks ', this.calculateTasks)
    console.log('####### this.$store.state ', this.$store.state)
  }
}
</script>

<style lang="scss" scoped>
.sidebar {
  border: 1px solid #f5f5f5;
  padding: 5px;
  border-radius: 5px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;

  &__title {
    padding: 5px 20px;
    width: 100%;
    border-bottom: 1px solid #f5f5f5;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
  }
  &__item{
    //width: 100%;
    padding: 8px;
    border-bottom: 1px solid #f5f5f5;
    cursor: pointer;
    &:hover {
      background-color: #f5f5f5;
    }
  }
}
.container{
  width: 100%;
}
</style>
