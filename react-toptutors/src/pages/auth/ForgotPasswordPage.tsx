import { Helmet } from 'react-helmet-async';
// sections
import Forgot from '../../sections/auth/Forgot';

// ----------------------------------------------------------------------

export default function ForgotPasswordPage() {
  return (
    <>
      <Helmet>
        <title> Forgot password | TopTutors</title>
      </Helmet>

      <Forgot />
    </>
  );
}
