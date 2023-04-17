<template>
  <div class="app-table">
    <div class="app-table__row">
      <div class="app-table__cell app-table__text">Категория</div>
      <div class="app-table__cell app-table__text">Кол-во (дес.)</div>
      <div class="app-table__cell app-table__text">Стоимость</div>
    </div>
    <div class="app-table__row line-hover" v-show="app.cB">
      <div class="app-table__cell">CB</div>
      <div class="app-table__cell">{{ app.cB }}</div>
      <div class="app-table__cell">{{ app.cB_cost }} ₽</div>
    </div>
    <div class="app-table__row line-hover" v-show="app.c0">
      <div class="app-table__cell">C0</div>
      <div class="app-table__cell">{{ app.c0 }}</div>
      <div class="app-table__cell">{{ app.c0_cost }} ₽</div>
    </div>
    <div class="app-table__row line-hover"  v-show="app.c1">
      <div class="app-table__cell">C1</div>
      <div class="app-table__cell">{{ app.c1 }}</div>
      <div class="app-table__cell">{{ app.c1_cost }} ₽</div>
    </div>
    <div class="app-table__row line-hover"  v-show="app.c2">
      <div class="app-table__cell">C2</div>
      <div class="app-table__cell">{{ app.c2 }}</div>
      <div class="app-table__cell">{{ app.c2_cost }} ₽</div>
    </div>
    <div class="app-table__row line-hover"  v-show="app.c3">
      <div class="app-table__cell">C3</div>
      <div class="app-table__cell">{{ app.c3 }}</div>
      <div class="app-table__cell">{{ app.c3_cost }} ₽</div>
    </div>
    <div class="app-table__row line-hover"  v-show="app.dirt">
      <div class="app-table__cell">Грязь</div>
      <div class="app-table__cell">{{ app.dirt }}</div>
      <div class="app-table__cell">{{ app.dirt_cost }} ₽</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TableEggs",
  props: ['app']
}
</script>

<style lang="scss" scoped>
.table {
  text-align: center;
  border: solid #ebebeb 3px;
  margin-bottom: 1rem;

  &__title {
    background-color: #f5f5f5;
  }
}

.app-table {
  display: flex;
  flex-direction: column;
  flex-flow: column;
  border: solid 2px #f3f3f3;
  border-radius: 15px;
  padding: 5px 10px;
  background-color: #fff;
  margin-bottom: 5px;

  &__title {
    width: 100%;
    height: 40px;
    margin: 0 auto;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    font-weight: 600;
    border: solid 2px #f3f3f3;
    border-bottom: 0;
    border-radius: 10px;
    background-color: #fff;
  }
  &__text {
    color: #c4c4c4;
  }
  &__row {
    width: 100%;
    display: inline-flex;
    justify-content: space-around;
    margin-bottom: 5px;
    gap: 3px;    
  }
  &__cell {
    width: 33%;
    text-align: center;
    border-bottom: solid 1.5px #eeeeee;
    border-radius: 5px;
  }
}

.line-hover {
  &:hover {
    background-color: #f5f5f5;
    border-radius: 5px;
  }
}
</style>