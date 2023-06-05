import axios from './axios';

export async function getLessonUrlStudent(id: number, setUrlForLesson: (value: string) => void) {
  await axios
    .get(`https://localhost:8080/api/get_lesson_space_url_student/${id}`)
    .then((response) => {
      setUrlForLesson(response.data.url);
    })
    .catch((error) => console.log(error));
}
export async function getLessonUrlTeacher(id: number, setUrlForLesson: (value: string) => void) {
  await axios
    .get(`https://localhost:8080/api/get_lesson_space_url_teacher/${id}`)
    .then((response) => {
      setUrlForLesson(response.data.url);
    })
    .catch((error) => console.log(error));
}
