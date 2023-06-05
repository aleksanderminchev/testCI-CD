import { Helmet } from 'react-helmet-async';
// sections
import Confirmation from '../../sections/auth/Confirmation';

// ----------------------------------------------------------------------

export default function ConfirmationPage() {
  return (
    <>
      <Helmet>
        <title> Confirm Profile | TopTutors</title>
      </Helmet>

      <Confirmation />
    </>
  );
}
