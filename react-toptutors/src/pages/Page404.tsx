import { Helmet } from 'react-helmet-async';
// assets
import Component404 from '../sections/auth/404';

// ----------------------------------------------------------------------

export default function Page404() {
  return (
    <>
      <Helmet>
        <title> 404 Page Not Found | TopTutors</title>
      </Helmet>

      <Component404 />
    </>
  );
}
