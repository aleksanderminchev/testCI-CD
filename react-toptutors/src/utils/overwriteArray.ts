/**
 * Function which appends new values and doesn't duplicate repeating values
 * @param list the initial list you want to append to
 * @param listToAdd the list you are adding to the first
 * @returns return an array, which has new values appended and old ones aren't duplicated
 */
export default function overwriteArray<T extends { id?: number | string }>(
  list: T[],
  listToAdd: T[]
): T[] {
  const elemsMapped = new Map(list.map((e) => [e.id, e]));
  const newList = listToAdd.forEach((e) => elemsMapped.set(e.id, e));

  return Array.from(elemsMapped.values());
}
